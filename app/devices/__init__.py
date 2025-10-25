from flask import Blueprint

# creamos la nueva bluepritn
device = Blueprint("device", __name__)

from app.devices import views