from flask import current_app

from models import db
from models.note import Note
from services.sync_service import SyncService
class NoteService:
	@staticmethod
	def can_read(note: Note, user_id: int | None) -> bool:
		if user_id is not None and note.owner_id == user_id:
			return True
		return note.visibility in ("read", "write")

	@staticmethod
	def can_write(note: Note, user_id: int | None) -> bool:
		if user_id is not None and note.owner_id == user_id:
			return True
		return note.visibility == "write"

	@staticmethod
	def create_note(owner_id: int, title: str, content: str = "", visibility: str = "private") -> Note:
		if not title or not title.strip():
			raise ValueError("Le titre ne peut pas être vide")
		
		if len(title) > 200:
			raise ValueError("Le titre ne peut pas dépasser 200 caractères")
		
		if len(content) > 10000:
			raise ValueError("Le contenu ne peut pas dépasser 10000 caractères")
		
		if visibility not in ["private", "read", "write"]:
			raise ValueError("Visibilité invalide")
		
		note = Note(owner_id=owner_id, title=title.strip(), content=content.strip(), visibility=visibility)
		db.session.add(note)
		db.session.commit()
		
		if current_app.config.get("SERVER_MODE") == "master":
			SyncService.sync_to_replica("create_note", {
				"id": note.id,
				"owner_id": owner_id,
				"title": title,
				"content": content,
				"visibility": visibility
			})
		return note

	@staticmethod
	def get_user_notes(user_id: int):
		return Note.query.filter_by(owner_id=user_id).all()

	@staticmethod
	def get_shared_public_notes(user_id: int):
		return (
			Note.query
			.filter(
				Note.owner_id != user_id,
				Note.visibility.in_(["read", "write"])
			)
			.all()
		)
	
	@staticmethod
	def can_user_read(note_id: int, user_id: int | None) -> bool:
		note = Note.query.filter_by(id=note_id).first()
		if note is None:
			return False
		if user_id is not None and note.owner_id == user_id:
			return True
		return note.visibility in ("read", "write")
	
	@staticmethod
	def get_note(note_id:int):
		return Note.query.filter_by(id=note_id).first()