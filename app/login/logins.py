import json
from flask import render_template, session, request, redirect, jsonify, url_for
from app.models.admin import db, Admins, TownAdmin
from . import logins


@logins.route('/loginve', methods=['POST'])
def loginve():
    if request.method == 'POST':
        username = request.json['name']
        password = request.json['pass']
        peter = Admins.query.filter_by(username=username, password=password).first()
        if peter:
            session['username'] = username
            # session['grade'] = peter.grade
            user1 = {"message": 1}
        else:
            user1 = {"message": 0}

        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}


@logins.route('/login/')
def login():
    return render_template('login.html')


@logins.route('/registered/')
def registered():
    return render_template('registered.html')




@logins.route('/town_loginve', methods=['POST'])
def town_loginve():
    if request.method == 'POST':
        username = request.json['name']
        password = request.json['pass']

        peter = TownAdmin.query.filter_by(username=username, password=password).first()
        if peter:
            session['town_name'] = username
            session['town_grade'] = peter.grade
            user1 = {"message": 1}
        else:
            user1 = {"message": 0}

        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}

@logins.route('/town_login/')
def town_login():
    return render_template('town_login.html')
