import os
from dotenv import load_dotenv

#carga de env
load_dotenv()

DEBUG = True
SECRET_KEY = 'secreto'
SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL")
#SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/database.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,       
    "pool_recycle": 1800,        
    "pool_timeout": 30,          
    "pool_size": 10,            
    "max_overflow": 5            
}

JWT_SECRET_KEY = 'supersecreto'
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS= ["access"]

JWT_TOKEN_LOCATION = ["cookies"]
JWT_COOKIE_SECURE = False # cambiar true en produccion
JWT_COOKIE_SAMESITE = "Lax"
JWT_COOKIE_HTTPONLY = True
JWT_ACCESS_COOKIE_NAME = "access_token_cookie"