from flask import Blueprint
admins = Blueprint('admins', __name__, template_folder='templates')
from app.admin import admins
from app.admin import adminimg
from app.admin import plateico
from app.admin import base
from app.admin import sjyimg
from app.admin import article
from app.admin import application
from app.admin import coordinate
