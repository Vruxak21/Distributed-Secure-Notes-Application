from flask import current_app
from models import db
from models.user import User
import bcrypt
from services.sync_service import SyncService

class UserService:
    @staticmethod
    def register(username: str, password: str):
        if not username or not password:
            raise ValueError("Nom et mdp requis")
        
        if len(password) < 6:
            raise ValueError("Le mot de passe doit contenir au moins 6 caractères")
        
        if len(username) < 3 or len(username) > 50:
            raise ValueError("Le nom d'utilisateur doit contenir entre 3 et 50 caractères")
        
        if User.query.filter_by(nom=username).first():
            raise ValueError("Ce nom d'utilisateur existe déjà")
        
        salt = bcrypt.gensalt()
        pswd_hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        pswd_string = pswd_hashed.decode('utf-8')

        user = User(nom=username, pswd_hashed=pswd_string)
        db.session.add(user)
        db.session.commit()

        if current_app.config.get("SERVER_MODE") == "master":
            SyncService.sync_to_replica("register_user", {
                "id": user.id,
                "nom": username,
                "pswd_hashed": pswd_string
            })
        return user

    @staticmethod
    def login(username: str, password: str):
        user = User.query.filter_by(nom=username).first()
        if user is None:
            return None
        if not bcrypt.checkpw(password.encode('utf-8'), user.pswd_hashed.encode('utf-8')):
            return None
        return user
    
    @staticmethod
    def get_user(user_id: int):
        return User.query.get(user_id)


