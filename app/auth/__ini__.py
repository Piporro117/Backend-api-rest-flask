import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# creacion de la base de datos
db: SQLAlchemy = SQLAlchemy()
bcrypt: Bcrypt = Bcrypt()
login_manager: LoginManager = LoginManager()
login_manager.login_view = "authentication.log_in_user"
login_manager.session_protection = "strong"

def create_app(config_type):
    app = Flask(__name__)
    configuration = os.path.join(os.getcwd(), "config", config_type + ".py")
    app.config.from_pyfile(configuration)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    from app.auth import authentication
    app.register_blueprint(authentication)
    return app
