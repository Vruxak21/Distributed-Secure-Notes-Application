# routes/users.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from services.user_service import UserService
import datetime

delta_time = 60 * 60 # Durée de validité du token en secondes

users_bp = Blueprint("api", __name__, url_prefix="/api")

@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    try:
        user = UserService.register(data.get("username"), data.get("password"))
        access_token = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(seconds=delta_time))
        response = jsonify({"success": True, "message": "Inscription réussie", "user": {"id": user.id, "username": user.nom}})
        set_access_cookies(response, access_token)
        return response, 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    user = UserService.login(data.get("username"), data.get("password"))
    if not user:
        return jsonify({"error": "invalid credentials"}), 401
    access_token = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(seconds=delta_time))
    response = jsonify({"success": True, "message": "Connexion réussie", "user": {"id": user.id, "username": user.nom}})
    set_access_cookies(response, access_token)
    return response, 200

@users_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = UserService.get_user(int(current_user_id))
    
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404
    
    return jsonify(logged_in_as=user.nom, user_id=current_user_id), 200

@users_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"success": True, "message": "Déconnexion réussie"})
    unset_jwt_cookies(response)
    return response, 200
