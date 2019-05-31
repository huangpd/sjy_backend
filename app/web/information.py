import json
import random
import time
from macpath import join
from flask import render_template, session, request, jsonify
from app.models.admin import db, Admins, Adminimg, Plateico, Base, Region, Sjyimg, Submit
from . import web

@web.route('/information/', methods=['POST'])
def information():
    if request.method == 'POST':
        gp = request.json['GP']
        phone = request.json['phone']
        base = request.json['base']
        username = request.json['username']
        timee = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        times = time.strftime("%Y%m%d%H%M%S", time.localtime())
        uid = str(random.randint(1000, 9999))  # str用于把数字转换成字符串
        uid = 'submit' + times + uid

        base = Base.query.filter(Base.uid == base).first()
        submit = Submit(uid=uid, gp=gp, phone=phone, username=username, base_name=base.name, base_uid=base.uid, times=timee)
        db.session.add(submit)
        db.session.commit()
        user1 = {"message": 1}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}