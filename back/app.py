from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import os

from models import db
from config import MasterConfig, ReplicaConfig
from routes.users import users_bp
from routes.notes import notes_bp
from routes.sync import sync_bp

def create_app(config_mode=None):
    app = Flask(__name__)
    
    server_mode = config_mode or os.environ.get('SERVER_MODE', 'master')

    if server_mode == 'master':
        app.config.from_object(MasterConfig)
    else:
        app.config.from_object(ReplicaConfig)
    
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
    app.register_blueprint(sync_bp)

    app.config['SERVER_MODE'] = server_mode

    print(app.url_map)

    return app

app = create_app()

if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))

    with app.app_context():
        # db.drop_all()  # A voir plus tard          
        db.create_all()
        print("Database tables created.")
    
    app.run(debug=True, port=port)
