import random
import time

from flask import session, jsonify
import json

from . import admins
import os
from flask import request
from werkzeug.utils import secure_filename
from pypinyin import pinyin, lazy_pinyin
from app.models.admin import db, Admins, Sjyimg

@admins.route('/sjyimgs/', methods=['POST'])
def sjyimgs():
    if request.method == 'POST':

        ff = request.files['file']
        filesname = "".join(lazy_pinyin(ff.filename))
        d = os.path.dirname(__file__)
        basepath = os.path.dirname(d)
        upload_path = os.path.join(basepath, 'static/uploads', secure_filename(filesname))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        ff.save(upload_path)
        url_st = '/static/uploads/' + secure_filename(filesname)

        name = ff.filename
        times = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        uid = str(random.randint(1000, 9999))   # str用于把数字转换成字符串
        uid = 'sjy'+ times + uid
        role = Sjyimg(uid=uid, url=url_st, grade=0, name=name)
        db.session.add(role)
        db.session.commit()

        return uid  # 文件的路径



@admins.route('/sjyimgdelete/', methods=['POST'])
def sjyimgdelete():
    if request.method == 'POST':
        uid = request.json['uid']
        sjyimg = db.session.query(Sjyimg).filter_by(uid=uid).first()
        db.session.delete(sjyimg)
        db.session.commit()
        user1 = {"message": 1}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}

