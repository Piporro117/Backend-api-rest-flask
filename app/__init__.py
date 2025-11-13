import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

#carga de env
load_dotenv()

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
    if config_type == "dev":
        CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
    else:
        CORS(app, supports_credentials=True, origins=[os.getenv("DOMAIN_URL")])


    from app.auth import authentication
    from app.devices import device
    from app.responses import response
    from app.gateways import gateway

    app.register_blueprint(authentication, url_prefix="/api/auth")
    app.register_blueprint(device, url_prefix="/api/device")
    app.register_blueprint(response, url_prefix="/api/response")
    app.register_blueprint(gateway, url_prefix="/api/gateway")

    return app
