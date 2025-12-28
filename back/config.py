class Config:
    SQLALCHEMY_DATABASE_URI =  'sqlite:///master.db'
    SQLALCHEMY_BINDS = {'replica': 'sqlite:///replica.db'}
    JWT_SECRET_KEY = 'xin-jojo-dome-island-party'  
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_CSRF_PROTECT = False