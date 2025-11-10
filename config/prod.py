import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = False
SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_recycle": 1800,
    "pool_timeout": 30,
    "pool_size": 10,
    "max_overflow": 5
}

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access"]

JWT_TOKEN_LOCATION = ["cookies"]
JWT_COOKIE_SECURE = True
JWT_COOKIE_SAMESITE = "None"
JWT_COOKIE_HTTPONLY = True
JWT_ACCESS_COOKIE_NAME = "access_token_cookie"
