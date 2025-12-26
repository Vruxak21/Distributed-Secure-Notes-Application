from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Enum, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import bcrypt

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True  #Pour les cookies/sessions
    }
})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///master.db'
app.config['SQLALCHEMY_BINDS'] = {'replica': 'sqlite:///replica.db'}

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(unique=True, nullable=False)
    pswd_hashed: Mapped[str] = mapped_column(nullable=False)

    notes_owned: Mapped[list["Note"]] = relationship("Note", back_populates="owner", cascade="all, delete-orphan")
    permissions: Mapped[list["Permission"]] = relationship("Permission", back_populates="user", cascade="all, delete-orphan")

class Note(db.Model):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[str] = mapped_column(server_default=func.current_date(), nullable=False)
    updated_at: Mapped[str] = mapped_column(server_default=func.current_date(), onupdate=func.current_date(), nullable=False)

    owner: Mapped[User] = relationship("User", back_populates="notes_owned")
    permissions: Mapped[list["Permission"]] = relationship("Permission", back_populates="note", cascade="all, delete-orphan")
    lock: Mapped["Lock"] = relationship("Lock", back_populates="note", uselist=False, cascade="all, delete-orphan")

class Permission(db.Model):
    __tablename__ = "permissions"

    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    access: Mapped[str] = mapped_column(
        Enum("read", "write", name="access_level", native_enum=False),
        nullable=False,
    )

    note: Mapped[Note] = relationship("Note", back_populates="permissions")
    user: Mapped[User] = relationship("User", back_populates="permissions")

class Lock(db.Model):
    __tablename__ = "locks"

    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    locked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    note: Mapped[Note] = relationship("Note", back_populates="lock")


@app.route('/tables')
def list_tables():
    tables = db.metadata.tables.keys()
    return "Tables available: " + ", ".join(tables)

# ---
# Login endpoint
# ---

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or request.form
    nom = data.get("username")
    pswd = data.get("password")

    if not nom or not pswd:
        return jsonify({"error": "username and password are required"}), 400

    user = User.query.filter_by(nom=nom).first()
    if user is None or not bcrypt.checkpw(pswd.encode('utf-8'), user.pswd_hashed.encode('utf-8')):
        return jsonify({"error": "invalid credentials"}), 401

    return jsonify({"message": "login ok"}), 200

    
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or request.form
    nom = data.get("username")
    pswd = data.get("password")

    if not nom or not pswd:
        return jsonify({"error": "username and password are required"}), 400

    existing = User.query.filter_by(nom=nom).first()
    if existing is not None:
        return jsonify({"error": "username already exists"}), 409

    salt = bcrypt.gensalt()
    pswd_hashed = bcrypt.hashpw(pswd.encode('utf-8'), salt)
    pswd_string = pswd_hashed.decode('utf-8')

    user = User(
        nom=nom,
        pswd_hashed=pswd_string
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "registered ok", "user_id": user.id}), 201

# ---
# Notes endpoints
# ---

@app.route('/api/notes/<int:user_id>', methods=['GET'])
def get_user_notes(user_id):
    """Récupère toutes les notes d'un utilisateur (owned + shared)"""
    try:
        # Notes appartenant à l'utilisateur
        owned_notes = Note.query.filter_by(owner_id=user_id).all()
        
        # Notes partagées avec l'utilisateur
        shared_permissions = Permission.query.filter_by(user_id=user_id).all()
        shared_note_ids = [p.note_id for p in shared_permissions]
        shared_notes = Note.query.filter(Note.id.in_(shared_note_ids)).all() if shared_note_ids else []
        
        notes_data = []
        
        # on formate les notes owned
        for note in owned_notes:
            notes_data.append({
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'created_at': note.created_at,
                'updated_at': note.updated_at,
                'is_owner': True,
                'access_level': 'write',
                'owner_name': note.owner.nom
            })
        
        # on formate les notes partagées
        for note in shared_notes:
            permission = next(p for p in shared_permissions if p.note_id == note.id)
            notes_data.append({
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'created_at': note.created_at,
                'updated_at': note.updated_at,
                'is_owner': False,
                'access_level': permission.access,
                'owner_name': note.owner.nom
            })
        
        return jsonify({
            'success': True,
            'notes': notes_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/note/<int:note_id>', methods=['GET'])
def get_note_detail(note_id):
    """Récupère les détails d'une note spécifique"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'user_id parameter is required'
            }), 400
        
        note = Note.query.get(note_id)
        
        if not note:
            return jsonify({
                'success': False,
                'error': 'Note not found'
            }), 404
        
        # on vérifie les permissions
        is_owner = note.owner_id == user_id
        permission = Permission.query.filter_by(note_id=note_id, user_id=user_id).first()
        
        if not is_owner and not permission:
            return jsonify({
                'success': False,
                'error': 'Access denied'
            }), 403
        
        # on vérifie le lock
        lock_info = None
        if note.lock:
            lock_info = {
                'is_locked': note.lock.locked,
                'locked_by_user_id': note.lock.user_id
            }
        
        return jsonify({
            'success': True,
            'note': {
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'created_at': note.created_at,
                'updated_at': note.updated_at,
                'is_owner': is_owner,
                'access_level': 'write' if is_owner else permission.access,
                'owner_name': note.owner.nom,
                'lock': lock_info
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)


with app.app_context():
    replica_engine = db.engines['replica']

    db.drop_all()                        
    db.metadata.drop_all(replica_engine)  

    db.create_all() 
    db.metadata.create_all(replica_engine)
    
    print("Master and Replica databases initialized!")