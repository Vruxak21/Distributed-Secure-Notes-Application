from flask import Blueprint, request, jsonify
from services.note_service import NoteService
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