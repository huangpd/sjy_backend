import random
import time

from flask import session, jsonify
import json

from . import admins
import os
from flask import request
from werkzeug.utils import secure_filename
from pypinyin import pinyin, lazy_pinyin
from app.models.admin import db, Base, Region

@admins.route('/base/', methods=['POST'])
def base():
    if request.method == 'POST':
        xy = request.json['XY']
        region = request.json['add']
        base = request.json['data']

        times = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        uid = str(random.randint(1000, 9999))  # str用于把数字转换成字符串
        uid = 'region' + times + uid



        regions = Region(uid=uid, xy=xy, region=region)
        bases = []
        for b in base:
            times = time.strftime("%Y%m%d-%H%M%S", time.localtime())
            uid = str(random.randint(1000, 9999))  # str用于把数字转换成字符串
            uid = 'base' + times + uid
            bas = Base(name=b['name'], text=b['text'], a=b['a'], h3=b['h3'], uid=uid)
            bases.append(bas)

        regions.base_url = bases
        db.session.add(regions)
        db.session.commit()
        return '123'


@admins.route('/base_v/', methods=['POST'])
def base_v():
    if request.method == 'POST':
        uid = request.json['uid']
        XY = request.json['XY']
        region = request.json['add']
        base = request.json['data']
        regions = db.session.query(Region).filter(Region.uid == uid).first()
        regions.xy = XY
        regions.region = region
        db.session.query(Base).filter(Base.region_id == uid).delete()
        bases = []
        for b in base:
            bas = Base(name=b['name'], text=b['text'], a=b['a'], h3=b['h3'], uid=b['uid'])
            bases.append(bas)
        regions.base_url = bases
        db.session.add(regions)
        db.session.commit()
        return '123'


@admins.route('/base_d/', methods=['POST'])
def base_d():
    if request.method == 'POST':
        uid = request.json['uid']
        print(uid)
        # db.session.query(Base).filter(Base.region_id == uid).delete()
        regions = db.session.query(Region).filter(Region.uid == uid).first()
        print(regions)
        db.session.delete(regions)
        db.session.commit()
        return '123'


