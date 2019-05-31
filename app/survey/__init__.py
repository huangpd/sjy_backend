from flask import Blueprint
survey = Blueprint('survey', __name__, template_folder='templates')
from app.survey import survey
from app.survey import form
