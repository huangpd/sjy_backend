from flask import render_template, session, redirect
from . import townss

@townss.route('/town_home/')
def town_home():
    return render_template('index.html')

@townss.route('/town_enter/')
def town_enter():
    return render_template('index.html')

@townss.route('/town_company/')
def town_company():
    return render_template('index.html')

@townss.before_request
def loginsif():
    if session.get('town_name') == None:
        return redirect('/town_login')
