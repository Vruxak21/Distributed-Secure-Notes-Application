from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Enregistrer les modeles SQLAlchemy
from .user import User
from .note import Note
from .lock import Lock

__all__ = ["db", "User", "Note", "Lock"]
