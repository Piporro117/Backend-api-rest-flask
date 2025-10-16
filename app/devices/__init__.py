from flask import Blueprint

# creamos la nueva bluepritn
devices = Blueprint("devices", __name__)

from app.devices import views