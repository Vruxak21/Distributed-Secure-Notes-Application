from models import db
from models.lock import Lock
from models.note import Note
from datetime import datetime, timedelta

class LockService:
    """Service to manage note locking in collaborative editing"""
    
    LOCK_TIMEOUT_MINUTES = 5  # Duration before automatic lock expiration
    
    @staticmethod
    def acquire_lock(note_id: int, user_id: int) -> dict:
        """
        Attempts to acquire a lock on a note for a user.
        Returns dict with success, message, and lock info
        """
        # Check that the note exists
        note = Note.query.get(note_id)
        if not note:
            return {"success": False, "error": "Note not found"}
        
        # Check write permissions
        from services.note_service import NoteService
        if not NoteService.can_write(note, user_id):
            return {"success": False, "error": "Write access denied"}
        
        # Find or create the lock
        lock = Lock.query.filter_by(note_id=note_id).first()
        
        if not lock:
            # Create new lock
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
        
        # If lock already exists
        if lock.locked:
            if lock.user_id == user_id:
                # Same user, renew the lock
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
                # Someone else has the lock
                return {
                    "success": False,
                    "error": "Note locked by another user",
                    "locked_by_user_id": lock.user_id
                }
        else:
            # Lock available, acquire it
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
        Releases the lock on a note.
        Only the lock owner or note owner can release.
        """
        lock = Lock.query.filter_by(note_id=note_id).first()
        
        if not lock or not lock.locked:
            return {"success": False, "error": "No active lock on this note"}
        
        # Check that it's the right user
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
        """Returns the lock status of a note"""
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
        Forces the release of a lock (admin or timeout).
        Use with caution.
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