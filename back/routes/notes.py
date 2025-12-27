from flask import Blueprint, jsonify, request
from services.note_service import NoteService

notes_bp = Blueprint("notes",__name__,url_prefix="/api")

@notes_bp.route('/users/<int:user_id>/notes', methods=['GET'])
def get_user_notes(user_id):
    """Récupère toutes les notes d'un utilisateur (owned + shared)"""
    try:
        # Notes appartenant à l'utilisateur
        owned_notes = NoteService.get_user_notes(user_id=user_id)
        
        # Notes partagées avec l'utilisateur
        shared_notes = NoteService.get_shared_public_notes(user_id=user_id)
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
                'visibility': note.visibility,
                'owner_name': note.owner.nom
            })
        
        # on formate les notes partagées
        for note in shared_notes:
            notes_data.append({
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'created_at': note.created_at,
                'updated_at': note.updated_at,
                'is_owner': False,
                'visibility': note.visibility,
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
        
        if not is_owner :
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
                'access_level': 'write' if is_owner else note.visibility,
                'owner_name': note.owner.nom,
                'lock': lock_info
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500