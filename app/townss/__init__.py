from flask import Blueprint
townss = Blueprint('townss', __name__, template_folder='../../myvue/dist', static_folder="../../myvue/dist", static_url_path='')
from app.townss import index
from app.townss import api
