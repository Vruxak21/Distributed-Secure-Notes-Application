from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import os
import logging
from logging.handlers import RotatingFileHandler

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

    return app

app = create_app()

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

@app.after_request
def set_security_headers(response):
    # Prévention Clickjacking
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    # Prévention MIME-type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # Protection XSS intégrée du navigateur
    response.headers['X-XSS-Protection'] = '1; mode=block'
    # Content Security Policy
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    # HSTS (décommenter en production HTTPS)
    # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Log requêtes sensibles
    if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
        app.logger.info(f'{request.method} {request.path} from {get_remote_address()}')
    
    return response

def setup_logging():
    if not app.debug:
        logs_dir = 'logs'
        try:
            os.makedirs(logs_dir, exist_ok=True)
        except OSError as e:
            logs_dir = f'logs_{app.config.get("SERVER_MODE", "unknown")}'
            os.makedirs(logs_dir, exist_ok=True)
        
        server_mode = app.config.get('SERVER_MODE', 'unknown')
        log_file = f'{logs_dir}/security_{server_mode}.log'
        
        file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            f'[{server_mode.upper()}] %(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info(f'{server_mode.capitalize()} server startup')

def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    with app.app_context():
        db.drop_all()  # A voir plus tard          
        db.create_all()
        print("Database tables created.")

        setup_logging()
    
    app.run(debug=True, port=port)
