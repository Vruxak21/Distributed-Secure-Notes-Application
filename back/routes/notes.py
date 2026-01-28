from flask import Blueprint, jsonify, request
from services.note_service import NoteService
from services.user_service import UserService
from services.lock_service import LockService
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


@notes_bp.route('/notes', methods=['GET'])
@jwt_required()
def get_user_notes_jwt():
    """Get all notes for the logged-in user (owned + shared)"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Notes owned by the user
        owned_notes = NoteService.get_user_notes(user_id=current_user_id)
        
        # Notes shared with the user
        shared_notes = NoteService.get_shared_public_notes(user_id=current_user_id)
        
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


@notes_bp.route('/users/<int:user_id>/notes', methods=['GET'])
def get_user_notes(user_id):
    """Get all notes for a user (owned + shared)"""
    try:
        # Notes owned by the user
        owned_notes = NoteService.get_user_notes(user_id=user_id)
        
        # Notes shared with the user
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
@jwt_required()
def get_note_detail(note_id):
    """Get details of a specific note"""
    try:
        current_user_id = int(get_jwt_identity())
        
        note = NoteService.get_note(note_id=note_id)
        
        if not note:
            return jsonify({
                'success': False,
                'error': 'Note not found'
            }), 404
        
        # Check permissions
        is_owner = note.owner_id == current_user_id
        can_read_note = NoteService.can_user_read(note.id, current_user_id)

        if not can_read_note:
            return jsonify({
                'success': False,
                'error': 'Access denied'
            }), 403
        
        # Get lock status
        lock_info = LockService.get_lock_status(note.id)
        
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

    current_user_id = int(get_jwt_identity())  # user id not in request
    data = request.get_json(silent=True) or {}

    # parameters
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


@notes_bp.route('/notes/<int:note_id>/lock', methods=['POST'])
@jwt_required()
def acquire_note_lock(note_id):
    """Acquire a lock on a note for editing"""
    try:
        current_user_id = int(get_jwt_identity())
        result = LockService.acquire_lock(note_id, current_user_id)
        
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 409  # Conflict
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@notes_bp.route('/notes/<int:note_id>/lock', methods=['DELETE'])
@jwt_required()
def release_note_lock(note_id):
    """Release the lock on a note"""
    try:
        current_user_id = int(get_jwt_identity())
        result = LockService.release_lock(note_id, current_user_id)
        
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 403
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@notes_bp.route('/notes/<int:note_id>/lock', methods=['GET'])
@jwt_required()
def get_note_lock_status(note_id):
    """Get the lock status of a note"""
    try:
        result = LockService.get_lock_status(note_id)
        return jsonify({
            "success": True,
            "lock": result
        }), 200
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@notes_bp.route('/notes/<int:note_id>/edit', methods=['PUT'])
@jwt_required()
def edit_note(note_id):
    current_user_id = int(get_jwt_identity())
    note = NoteService.get_note(note_id=note_id)
    if not note:
        return jsonify({"error": "note not found"}), 404

    data = request.get_json(silent=True) or {}

    # params
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()

    if not title or not content:
        return jsonify({"error": "invalid note data"}), 400

    try:
        note = NoteService.get_note(note_id=note_id)
        if not note:
            return jsonify({"error": "note not found"}), 404

        if note.owner_id != current_user_id and not NoteService.can_write(note, current_user_id):
            return jsonify({"error": "access denied"}), 403

        updated_note = NoteService.update_note(
            note_id,
            title,
            content
        )
    
        result = LockService.release_lock(note_id, current_user_id)
        if not result["success"]:
            return jsonify({"error": "could not release lock"}), 403
    
        if not updated_note:
            return jsonify({"error": "could not update note"}), 400

        return jsonify({"success": True, "note": serialize_note(updated_note, True)}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@notes_bp.route('/notes/<int:note_id>/edit', methods=['GET'])
@jwt_required()
def get_note_for_edit(note_id):
    current_user_id = int(get_jwt_identity())
    note = NoteService.get_note(note_id=note_id)
    if not note:
        return jsonify({"error": "note not found"}), 404
    
    if note.owner_id != current_user_id and not NoteService.can_write(NoteService.get_note(note_id), current_user_id):
        return jsonify({"error": "access denied"}), 403
    
    lock_info = LockService.get_lock_status(note.id)
    if lock_info['locked'] and lock_info['user_id'] != current_user_id:
        return jsonify({"error": "note is locked by another user"}), 409
    else:
        result = LockService.acquire_lock(note.id, current_user_id)
        if not result["success"]:
            return jsonify({"error": "could not acquire lock"}), 409
        
    return jsonify({
        "success": True,
        "note": serialize_note(note, True)
    }), 200