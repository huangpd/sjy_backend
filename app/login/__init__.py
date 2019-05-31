from flask import Blueprint
logins = Blueprint('logins', __name__, template_folder='templates')
from app.login import logins
