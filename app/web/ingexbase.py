import json
import time
from macpath import join
from flask import render_template, session, request, jsonify
from app.models.admin import db, Admins, Adminimg, Plateico, Base, Region, Sjyimg
from . import web

@web.route('/ingexbase/', methods=['POST'])
def ingexbase():
    if request.method == 'POST':
        uid = request.json['uid']
        base = db.session.query(Region).filter(Region.uid == uid).first().base_url
        data = data = jsonify(bedict1(base))
        return data, 200, {"ContentType": "application/json"}

def bedict1(a):
    lic = []
    for text in a:
        lic.append(
            {
                'id': text.id,
                'name': text.name,
                'text': text.text,
                'h3': text.h3,
                'a': text.a
            }
        )
    return lic
