from flask import Blueprint, jsonify, request
from services.note_service import NoteService
from services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity
notes_bp = Blueprint("notes",__name__,url_prefix="/api")


def serialize_note(note, is_owner: bool):
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at,
        "updated_at": note.updated_at,
        "is_owner": is_owner,
        "visibility": note.visibility,
        "owner_name": note.owner.nom,
    }


@notes_bp.route('/users/<int:user_id>/notes', methods=['GET'])
def get_user_notes(user_id):
    """Récupère toutes les notes d'un utilisateur (owned + shared)"""
    try:
        # Notes appartenant à l'utilisateur
        owned_notes = NoteService.get_user_notes(user_id=user_id)
        
        # Notes partagées avec l'utilisateur
        shared_notes = NoteService.get_shared_public_notes(user_id=user_id)
        notes_data = []
        
        notes_data = [
            serialize_note(note, True)
            for note in owned_notes
        ] + [
            serialize_note(note, False)
            for note in shared_notes
        ]
        
        return jsonify({
            'success': True,
            'notes': notes_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@notes_bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note_detail(note_id):
    """Récupère les détails d'une note spécifique"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'user_id parameter is required'
            }), 400
        
        note = NoteService.get_note(note_id=note_id)
        
        if not note:
            return jsonify({
                'success': False,
                'error': 'Note not found'
            }), 404
        
        # on vérifie les permissions
        is_owner = note.owner_id == user_id
        can_read_note = NoteService.can_user_read(note.id,user_id)

        if not can_read_note :
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
                **serialize_note(note, is_owner),
                'access_level': 'write' if is_owner else note.visibility,
                'lock': lock_info,
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    

@notes_bp.route('/notes', methods=["POST"])
@jwt_required()
def add_new_note():

    current_user_id = int(get_jwt_identity())  # id du user pas dans la requete
    data = request.get_json(silent=True) or {}

    # params
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()
    visibility = (data.get("visibility") or "").strip()

    allowed_visibility = {"private", "read", "write"}
    if not title or not content or visibility not in allowed_visibility:
        return jsonify({"error": "invalid note data"}), 400

    try:
        user = UserService.get_user(user_id=current_user_id)
        if not user:
            return jsonify({"error": "invalid user"}), 400

        note = NoteService.create_note(
            current_user_id,
            title,
            content,
            visibility)
        if not note:
            return jsonify({"error": "invalid note information"}), 400
            
        return jsonify({"success": True, "note": serialize_note(note, True)}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400




