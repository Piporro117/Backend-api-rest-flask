import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# creacion de la base de datos
db: SQLAlchemy = SQLAlchemy()
bcrypt: Bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_type):
    app = Flask(__name__)
    configuration = os.path.join(os.getcwd(), "config", config_type + ".py")
    app.config.from_pyfile(configuration)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"]) # permiritr que envie cualqier persona


    from app.auth import authentication
    app.register_blueprint(authentication, url_prefix="/api/auth")
    return app
