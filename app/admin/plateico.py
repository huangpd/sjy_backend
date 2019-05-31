import random
import time

from flask import session, jsonify
import json

from . import admins
import os
from flask import request
from werkzeug.utils import secure_filename
from pypinyin import pinyin, lazy_pinyin
from app.models.admin import db, Plateico


@admins.route('/platein/', methods=['POST'])
def platein():
    # rq_data = request.json
    # User.create(**rq_data)
    # return jsonify({'code': 200, 'data':{'msg': 'chuanjian'}})
    if request.method == 'POST':
        ico = request.json['ico']
        name = request.json['name']
        text = request.json['text']
        url = request.json['url']

        role = Plateico(ico=ico, name=name, text=text, url=url)
        db.session.add(role)
        db.session.commit()

        t={
                'id': role.id,
                'ico': ico,
                'name': name,
                'text': text,
                'url': url,
            }

        data = jsonify(t)
        return data, 200, {"ContentType": "application/json"}


@admins.route('/platedelete/', methods=['POST'])
def platedelete():
    if request.method == 'POST':
        id = request.json['id']

        platedelete = db.session.query(Plateico).filter_by(id=id).first()
        db.session.delete(platedelete)
        db.session.commit()
        user1 = {"message": 1}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}



