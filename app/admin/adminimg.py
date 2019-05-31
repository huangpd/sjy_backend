import random
import time

from qiniu import Auth, put_file, etag
import qiniu.config


from flask import session, jsonify
import json

from . import admins
import os
from flask import request
from werkzeug.utils import secure_filename
from pypinyin import pinyin, lazy_pinyin
from app.models.admin import db, Admins, Adminimg

@admins.route('/adminimgs/', methods=['POST'])
def adminimgs():
    if request.method == 'POST':

        ff = request.files['file']
        filesname = "".join(lazy_pinyin(ff.filename))
        d = os.path.dirname(__file__)
        basepath = os.path.dirname(d)
        upload_path = os.path.join(basepath, 'static/uploads', secure_filename(filesname))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        ff.save(upload_path)


        times = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        uid = str(random.randint(1000, 9999))  # str用于把数字转换成字符串
        uid = times + uid
        name = ff.filename



        m = secure_filename(filesname)
        sname = uid + m
        # 需要填写你的 Access Key 和 Secret Key
        access_key = 'SvHVcX7ZotlGtp7Lpxy1Az95Ae_tC8lOqnC02A9C'
        secret_key = 'blSArZE6UCrYABtjaYwTFLHeBXCeofUKjpoEKspi'
        # 构建鉴权对象
        q = Auth(access_key, secret_key)
        # 要上传的空间
        bucket_name = '51shuimu'
        # 上传后保存的文件名
        key = sname
        token = q.upload_token(bucket_name, key, 3600)
        localfile = upload_path
        ret, info = put_file(token, key, localfile)
        assert ret['key'] == key
        assert ret['hash'] == etag(localfile)
        url_st = 'http://pqcmnd3qt.bkt.clouddn.com/'+sname



        role = Adminimg(uid=uid, url=url_st, grade=0, name=name)
        db.session.add(role)
        db.session.commit()

        return uid  # 文件的路径

# @admins.route('/qiniuyun_img/', methods=['POST','GET'])
# def qiniuyun_img():
#     filename = request.get['filename']
#     print (filename)




@admins.route('/adminimgll', methods=['POST'])
def adminimgll():
    if request.method == 'POST':
        uid = request.json['uid']
        a = request.json['a']
        adminimg = db.session.query(Adminimg).filter_by(uid=uid).first()
        adminimg.a = a
        db.session.commit()
        user1 = {"message": 1}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}





@admins.route('/adminimgdelete', methods=['POST'])
def adminimgdelete():
    if request.method == 'POST':
        uid = request.json['uid']
        adminimg = db.session.query(Adminimg).filter_by(uid=uid).first()
        db.session.delete(adminimg)
        db.session.commit()
        user1 = {"message": 1}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}

