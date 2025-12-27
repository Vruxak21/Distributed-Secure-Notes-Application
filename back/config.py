class Config:
    SQLALCHEMY_DATABASE_URI =  'sqlite:///master.db'
    SQLALCHEMY_BINDS = {'replica': 'sqlite:///replica.db'}
    JWT_SECRET_KEY = 'xin-jojo-dome-island-party'  