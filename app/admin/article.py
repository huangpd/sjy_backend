import random
import time

from flask import session, jsonify
import json

from . import admins
import os
from flask import request
from werkzeug.utils import secure_filename
from pypinyin import pinyin, lazy_pinyin
from app.models.admin import db, Label, Article


@admins.route('/titlein/', methods=['POST'])
def titlein():
    if request.method == 'POST':
        value = request.json['value']
        times = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        uid = str(random.randint(1000, 9999))  # str用于把数字转换成字符串
        uid = 'Label' + times + uid

        role = Label(uid=uid, value=value)
        db.session.add(role)
        db.session.commit()
        t = {
                'id': role.id,
                'uid': uid,
                'value': value,
            }

        data = jsonify(t)
        return data, 200, {"ContentType": "application/json"}


@admins.route('/titlein_delete/', methods=['POST'])
def titlein_delete():
    if request.method == 'POST':
        uid = request.json['uid']
        label = db.session.query(Label).filter(Label.uid == uid).first()
        db.session.delete(label)
        db.session.commit()

        session['articlaeimg'] = None
        user1 = {"value": 1, "message": '数据彻底删除！'}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}











@admins.route('/articlaeimg/', methods=['POST'])
def articlaeimg():
    if request.method == 'POST':
        ff = request.files['file']
        filesname = "".join(lazy_pinyin(ff.filename))
        d = os.path.dirname(__file__)
        basepath = os.path.dirname(d)
        upload_path = os.path.join(basepath, 'static/article_img', secure_filename(filesname))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        ff.save(upload_path)
        url_st = '/static/article_img/' + secure_filename(filesname)
        session['articlaeimg'] = url_st


        data = jsonify(url_st)
        return data, 200, {"ContentType": "application/json"}


@admins.route('/articlaes/', methods=['POST'])
def articlaes():
    if request.method == 'POST':
        date = request.json['date']
        html = request.json['html']
        label = request.json['label']
        texts = request.json['text']
        title = request.json['title']
        tt = request.json['tt']
        img_url = session['articlaeimg']

        if session.get('articlaeimg') == None:
            user1 = {"value" : 0,"message":'请上传图片！'}
            data = json.dumps(user1)
            return data, 200, {"ContentType": "application/json"}


        times = time.strftime("%Y%m%d%H%M%S", time.localtime())
        uid = str(random.randint(1000, 9999))  # str用于把数字转换成字符串
        uid = 'art' + times + uid


        label = db.session.query(Label).filter(Label.uid == label).first()
        role = Article(date=date, html=html, texts=texts, title=title, tt=tt, img_url=img_url, uid=uid, label_value=label.value, label_uid=label.uid, label_id=label.id)

        db.session.add(role)
        db.session.commit()


        session['articlaeimg'] = None
        user1 = {"value": 1, "message": '上传成功过！'}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}



@admins.route('/art_delete/', methods=['POST'])
def art_delete():
    if request.method == 'POST':
        uid = request.json['uid']
        article = db.session.query(Article).filter(Article.uid == uid).first()

        article.deletes = 0
        db.session.commit()

        session['articlaeimg'] = None
        user1 = {"value": 1, "message": '移入垃圾箱成功！'}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}

@admins.route('/art_ds/', methods=['POST'])
def art_ds():
    if request.method == 'POST':
        uid = request.json['uid']
        article = db.session.query(Article).filter(Article.uid == uid).first()

        article.deletes = 1
        db.session.commit()

        session['articlaeimg'] = None
        user1 = {"value": 1, "message": '数据回复成功！'}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}



@admins.route('/art_deletes/', methods=['POST'])
def art_deletes():
    if request.method == 'POST':
        uid = request.json['uid']
        article = db.session.query(Article).filter(Article.uid == uid).first()

        db.session.delete(article)
        db.session.commit()

        session['articlaeimg'] = None
        user1 = {"value": 1, "message": '数据彻底删除！'}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}



















@admins.route('/articlaell/', methods=['POST'])
def articlaell():
    if request.method == 'POST':
        date = request.json['date']
        html = request.json['html']
        label = request.json['label']
        texts = request.json['text']
        title = request.json['title']
        tt = request.json['tt']
        uid = request.json['uid']
        label = db.session.query(Label).filter(Label.uid == label).first()
        article = Article.query.filter(Article.uid == uid).first()
        print(article)


        article.date = date
        article.html = html
        article.texts = texts
        article.title = title
        article.tt = tt
        article.label_value =label.value
        article.label_uid =label.uid
        article.label_id =label.id
        if session.get('articlaeimg') != None:
            img_url = session['articlaeimg']
            article.img_url = img_url
        db.session.commit()


        session['articlaeimg'] = None
        user1 = {"value": 1, "message": '上传成功过！'}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}