from flask import Blueprint, request, jsonify
from models import db, Note, User

sync_bp = Blueprint("sync", __name__, url_prefix="/api/sync")

@sync_bp.route("/create_note", methods=["POST"])
def sync_create_note():
    data = request.get_json() or {}

    try:
        note = Note(
            id=data["id"],
            owner_id=data["owner_id"],
            title=data["title"],
            content=data["content"],
            visibility=data["visibility"]
        )

        db.session.add(note)
        db.session.commit()

        return jsonify({"success": True}), 201
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    
@sync_bp.route("/register_user", methods=["POST"])
def sync_register_user():
    data = request.get_json() or {}

    try:
        user = User(
            id=data["id"],
            nom=data["nom"],
            pswd_hashed=data["pswd_hashed"]
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"success": True}), 201
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    

@sync_bp.route("/update_note", methods=["POST"])
def sync_update_note():
    data = request.get_json() or {}

    try: 
        title = data.get("title")
        content = data.get("content")
        note_id = data.get("id")

        updated_note = Note.query.filter_by(id=note_id).first()
        if updated_note:
            updated_note.title = title
            updated_note.content = content
            db.session.commit()

        if not updated_note:
            print("Could not update note - not found")
            return jsonify({"error": "could not update note"}), 400

        return jsonify({"success": True}), 200

    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)}), 400
