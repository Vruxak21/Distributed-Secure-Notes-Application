from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db

from routes.users import users_bp
from routes.notes import notes_bp

import os

app = Flask(__name__)

# Database configuration
app.config.from_object(Config)
# Cors 
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True  #Pour les cookies/sessions
    }
})

db.init_app(app)
jwt = JWTManager(app)

#ne pas oublier d'ajouter chaque blue print sinon les routes seront pas prises en compte
app.register_blueprint(users_bp)
app.register_blueprint(notes_bp)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)


with app.app_context():
    db.drop_all()                
    db.create_all()
    print("Database tables created.")