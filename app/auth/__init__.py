from flask import Blueprint

# creamos la nueva bluepritn
authentication = Blueprint("authentication", __name__)

from app.auth import views
