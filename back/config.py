import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')  
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_CSRF_PROTECT = False

    SERVER_MODE = os.environ.get('SERVER_MODE', 'master')
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        if self.SERVER_MODE == 'master':
            return os.environ.get('DATABASE_URI', 'sqlite:///master.db')
        else:
            return os.environ.get('DATABASE_REPLICA_URI', 'sqlite:///replica.db')

class MasterConfig(Config):
    SERVER_MODE = 'master'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///master.db')

class ReplicaConfig(Config):
    SERVER_MODE = 'replica'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_REPLICA_URI', 'sqlite:///replica.db')