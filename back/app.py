from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from models import db

from routes.users import users_bp
from routes.notes import notes_bp
import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)

# Database configuration
app.config.from_object(Config)

# JWT Configuration pour cookies httpOnly
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # False en dev (True en prod avec HTTPS)
app.config['JWT_COOKIE_SECURE'] = False  # False en dev HTTP, True en prod HTTPS
app.config['JWT_COOKIE_SAMESITE'] = 'Lax'  # Protection CSRF
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_COOKIE_DOMAIN'] = None  # None pour localhost

# Rate Limiting Configuration
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Logging Configuration
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/security.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')

# Cors 
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True  #Pour les cookies/sessions
    }
})

# Security Headers
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

db.init_app(app)
jwt = JWTManager(app)

#ne pas oublier d'ajouter chaque blue print sinon les routes seront pas prises en compte
app.register_blueprint(users_bp)
app.register_blueprint(notes_bp)


def init_db():
    """Initialise la base de données (à appeler manuellement)"""
    with app.app_context():
        replica_engine = db.engines['replica']
        db.create_all() 
        db.metadata.create_all(replica_engine)
        print("Master and Replica databases initialized!")

def reset_db():
    """DANGER: Réinitialise complètement la base de données (DEV ONLY)"""
    with app.app_context():
        replica_engine = db.engines['replica']
        db.drop_all()                        
        db.metadata.drop_all(replica_engine)  
        db.create_all() 
        db.metadata.create_all(replica_engine)
        print("⚠️  ATTENTION: Base de données réinitialisée!")

if __name__ == '__main__':
    # Initialiser la BD sans la réinitialiser
    with app.app_context():
        replica_engine = db.engines['replica']
        db.create_all() 
        db.metadata.create_all(replica_engine)
        print("Database ready (tables created if not exist)")
    
    app.run(debug=True, port=5000)