from flask import Blueprint

# creamos la nueva bluepritn
response = Blueprint("response", __name__)

from app.responses import views