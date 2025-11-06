from flask import Blueprint

# creamos la nueva bluepritn
gateway = Blueprint("gateway", __name__)

from app.gateways  import views