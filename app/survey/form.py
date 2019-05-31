import json
import random
import time
from . import survey
from flask import request
from app.models.admin import db, Base, Forms
@survey.route('/forms/', methods=['POST'])
def forms():
    if request.method == 'POST':
        company_genre = request.json['company_genre']
        demand = request.json['demand']
        demand_text = request.json['demand_text']
        phone = request.json['phone']
        policy = request.json['policy']
        policy_s = request.json['policy_s']
        position = request.json['position']
        taxes = request.json['taxes']
        text = request.json['text']

        times = time.strftime("%Y%m%d%H%M%S", time.localtime())
        uid = str(random.randint(1000, 9999))  # str用于把数字转换成字符串
        uid ='form' + times + uid
        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        print(demand_text)
        y = 0
        demand_texts = []
        for i in demand_text:
            if i != None:
                key = demand[y]
                y = y+1
                data = key + ':' + i
                demand_texts.append(data)

        demand_texts = fien(demand_texts)


        if policy_s:
            policy.append(policy_s)

        policy = fien(policy)

        forms = Forms(company_genre=company_genre, demand=demand_texts, phone=phone, position=position, taxes=taxes, text=text, policy=policy, uid=uid, times=times, status=0)

        db.session.add(forms)
        db.session.commit()

        user1 = {"value": 1, "message": '提交成功！'}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}

def fien(v):
    ss = ''
    for i in v:
        ss = ss + i + '; '
    return ss




@survey.route('/forms_v/', methods=['POST'])
def forms_v():
    if request.method == 'POST':
        uid = request.json['uid']
        submit = db.session.query(Forms).filter_by(uid=uid).first()
        if submit.status == 0:
            submit.status = 1
        else:
            submit.status = 0
        db.session.commit()

        user1 = {"message": 1}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}\

@survey.route('/forms_d/', methods=['POST'])
def forms_d():
    if request.method == 'POST':
        uid = request.json['uid']
        submit = db.session.query(Forms).filter_by(uid=uid).first()
        db.session.delete(submit)
        db.session.commit()
        user1 = {"message": 1}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}