import random
import time

from flask import session, jsonify
import json

from . import admins
import os
from flask import request
from werkzeug.utils import secure_filename
from pypinyin import pinyin, lazy_pinyin
from app.models.admin import db, Plateico, Submit


@admins.route('/applications/', methods=['POST'])
def applications():
    if request.method == 'POST':
        uid = request.json['uid']
        submit = db.session.query(Submit).filter_by(uid=uid).first()
        if submit.status == 0:
            submit.status = 1
        else:
            submit.status = 0
        db.session.commit()

        user1 = {"message": 1}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}



