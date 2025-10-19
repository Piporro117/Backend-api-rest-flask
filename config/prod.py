# prod.py
DEBUG = False  # nunca en True en producción
SECRET_KEY = 'una_clave_muy_segura_y_larga'
SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/database.db"  # si migras a PostgreSQL/MySQL, cambiar aquí
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT
JWT_SECRET_KEY = 'otra_clave_muy_segura_y_larga'
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access"]

JWT_TOKEN_LOCATION = ["cookies"]
JWT_COOKIE_SECURE = True         # obligatorio en producción con HTTPS
JWT_COOKIE_SAMESITE = "None"     # permite cookies cross-site si tu front está en otro dominio
JWT_COOKIE_HTTPONLY = True       # evita acceso desde JS
JWT_ACCESS_COOKIE_NAME = "access_token_cookie"


# produccion segun investigacio
# DEBUG = False
# SECRET_KEY = 'clave-segura-produccion'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario:password@host/nombre_bd'
# SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT_SECRET_KEY = 'clave-super-secreta'
# JWT_TOKEN_LOCATION = ["cookies"]
# JWT_COOKIE_SECURE = True   # True en producción
# JWT_COOKIE_SAMESITE = "None"
# JWT_COOKIE_HTTPONLY = True
# JWT_ACCESS_COOKIE_NAME = "access_token_cookie"
