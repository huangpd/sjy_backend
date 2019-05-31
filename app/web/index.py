from flask import render_template, session, request
from app.models.admin import db, Admins, Adminimg, Plateico, Base, Region, Sjyimg, Article, Label
from . import web


@web.route('/')
def index():
    adminimg = db.session.query(Adminimg).all()
    sjyimgs = db.session.query(Sjyimg).all()
    plateico = db.session.query(Plateico).all()
    base = db.session.query(Region).filter(Region.id == 1).first().base_url
    region = db.session.query(Region).all()
    return render_template('indexs.html', adminimg=adminimg, plateico=plateico, base=base, region=region, sjyimgs=sjyimgs)


@web.route('/research/', methods=['post', 'get'])
def research():

    page = request.args.get('page', 1, type=int)
    uid = request.args.get('uid')
    if uid:




        label = db.session.query(Label).all()

        article =Label.query.filter(Label.uid == uid, Article.deletes == 1).first().article_url

        pagination=''

    else:
        label = db.session.query(Label).all()
        pagination = Article.query.filter_by(deletes=1).order_by(Article.date.desc()).paginate(page=page, per_page=5)
        article = pagination.items


    return render_template('research.html', article=article, label=label, pagination=pagination)


@web.route('/submit/')
def submit():
    region = db.session.query(Region).all()
    base = db.session.query(Base).all()
    return render_template('submit.html', region=region,  base=base, )


@web.route('/articles/')
def articles():
    uid = request.args.get('uid')
    article = Article.query.filter(Article.uid == uid).first()
    return render_template('articles.html', article=article)


