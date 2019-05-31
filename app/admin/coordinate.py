import random
import time
from flask import session, jsonify
from . import admins
from flask import request
from app.models.admin import db, Label, Article, Region


@admins.route('/coordinates/', methods=['POST'])
def coordinates():
    if request.method == 'POST':
        uid = request.json['uid']

        region = db.session.query(Region).filter(Region.uid == uid).first()
        base = region.base_url


        region = region.to_json()
        bases = []
        for x in base:
            bases.append(x.to_json())

        data = {
            'region': region,
            'base': bases,
        }
        print(data)
        data = jsonify(data)
        return data, 200, {"ContentType": "application/json"}
