from flask import render_template, session, request, redirect
from app.models.admin import db,Forms
from . import survey

@survey.route('/survey/surveys/')
def surveys():

    return render_template('survey.html')

@survey.route('/survey/surveys/admin')
def surveys_admin():
    forms = db.session.query(Forms).all()
    return render_template('surveys_admin.html',forms=forms)

@survey.route('/survey/surveys/MP_verify_tWcNIB4BjtVOus8j.txt')
def sign_ups2():
    return 'tWcNIB4BjtVOus8j'