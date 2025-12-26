from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Enum, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///master.db'
app.config['SQLALCHEMY_BINDS'] = {'replica': 'sqlite:///replica.db'}

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(unique=True, nullable=False)
    pswd_hashe: Mapped[str] = mapped_column(nullable=False)

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


with app.app_context():
    replica_engine = db.engines['replica']

    db.drop_all()                        
    db.metadata.drop_all(replica_engine)  

    db.create_all() 
    db.metadata.create_all(replica_engine)
    
    print("Master and Replica databases initialized!")

