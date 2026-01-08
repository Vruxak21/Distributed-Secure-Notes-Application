from models import db
from models.lock import Lock
from models.note import Note
from datetime import datetime, timedelta

class LockService:
    """Service pour gérer le verrouillage des notes en édition collaborative"""
    
    LOCK_TIMEOUT_MINUTES = 5  # durée avant expiration automatique du lock
    
    @staticmethod
    def acquire_lock(note_id: int, user_id: int) -> dict:
        """
        Tente d'acquérir un lock sur une note pour un utilisateur.
        Retourne dict avec success, message, et info du lock
        """
        # on vérifie que la note existe
        note = Note.query.get(note_id)
        if not note:
            return {"success": False, "error": "Note not found"}
        
        # on vérifie les permissions d'écriture
        from services.note_service import NoteService
        if not NoteService.can_write(note, user_id):
            return {"success": False, "error": "Write access denied"}
        
        # on cherche ou crée le lock
        lock = Lock.query.filter_by(note_id=note_id).first()
        
        if not lock:
            # on crée nouveau lock
            lock = Lock(note_id=note_id, user_id=user_id, locked=True)
            db.session.add(lock)
            db.session.commit()
            return {
                "success": True,
                "message": "Lock acquired",
                "lock": {
                    "note_id": note_id,
                    "user_id": user_id,
                    "locked": True
                }
            }
        
        # si le lock existe déjà
        if lock.locked:
            if lock.user_id == user_id:
                #même utilisateur, renouveler le lock
                return {
                    "success": True,
                    "message": "Lock renewed",
                    "lock": {
                        "note_id": note_id,
                        "user_id": user_id,
                        "locked": True
                    }
                }
            else:
                # qqn d'autre a le lock
                return {
                    "success": False,
                    "error": "Note locked by another user",
                    "locked_by_user_id": lock.user_id
                }
        else:
            # lock disponible, l'acquérir
            lock.locked = True
            lock.user_id = user_id
            db.session.commit()
            return {
                "success": True,
                "message": "Lock acquired",
                "lock": {
                    "note_id": note_id,
                    "user_id": user_id,
                    "locked": True
                }
            }
    
    @staticmethod
    def release_lock(note_id: int, user_id: int) -> dict:
        """
        Libère le lock d'une note.
        Seul le propriétaire du lock ou le propriétaire de la note peut libérer.
        """
        lock = Lock.query.filter_by(note_id=note_id).first()
        
        if not lock or not lock.locked:
            return {"success": False, "error": "No active lock on this note"}
        
        # on vérifie que c'est le bon utilisateur
        note = Note.query.get(note_id)
        if lock.user_id != user_id and note.owner_id != user_id:
            return {"success": False, "error": "Cannot release lock owned by another user"}
        
        lock.locked = False
        lock.user_id = None
        db.session.commit()
        
        return {
            "success": True,
            "message": "Lock released"
        }
    
    @staticmethod
    def get_lock_status(note_id: int) -> dict:
        """Retourne l'état du lock d'une note"""
        lock = Lock.query.filter_by(note_id=note_id).first()
        
        if not lock:
            return {
                "note_id": note_id,
                "locked": False,
                "user_id": None
            }
        
        return {
            "note_id": note_id,
            "locked": lock.locked,
            "user_id": lock.user_id
        }
    
    @staticmethod
    def force_release_lock(note_id: int) -> dict:
        """
        Force la libération d'un lock (admin ou timeout).
        À utiliser avec précaution.
        """
        lock = Lock.query.filter_by(note_id=note_id).first()
        
        if not lock:
            return {"success": False, "error": "No lock found"}
        
        lock.locked = False
        lock.user_id = None
        db.session.commit()
        
        return {
            "success": True,
            "message": "Lock forcefully released"
        }