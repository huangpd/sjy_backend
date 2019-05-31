from flask import Blueprint
web = Blueprint('web', __name__, template_folder='templates')
from app.web import index
from app.web import ingexbase
from app.web import information
