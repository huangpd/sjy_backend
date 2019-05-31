
from flask import render_template, session, request, redirect

from app.models.admin import db, Admins, Adminimg, Plateico, Base, Region, Sjyimg, Label, Article, Submit
from . import admins

@admins.route('/admin/')
def admin():
    adminimg = db.session.query(Adminimg).all()
    sjyimgs = db.session.query(Sjyimg).all()
    plateico = db.session.query(Plateico).all()
    region = db.session.query(Region).all()

    if region:
        base = db.session.query(Region).filter(Region.id == 1).first().base_url
        return render_template('admin.html', adminimg=adminimg, plateico=plateico, region=region, sjyimgs=sjyimgs, base=base)
    else:
        return render_template('admin.html', adminimg=adminimg, plateico=plateico, region=region, sjyimgs=sjyimgs)

@admins.route('/article/')
def article():

    label = db.session.query(Label).all()

    return render_template('article.html', label=label,)

@admins.route('/article_all/')
def article_all():
    article = db.session.query(Article).filter(Article.deletes == 1).all()
    return render_template('article_all.html', article=article,)


@admins.route('/article_delete/')
def article_delete():
    article = db.session.query(Article).filter(Article.deletes == 0).all()
    return render_template('article_delete.html', article=article,)


@admins.route('/article_ll/')
def article_ll():
    label = db.session.query(Label).all()
    uid = request.args['uid']
    article =db.session.query(Article).filter(Article.uid == uid).first()

    return render_template('article_ll.html', article=article, label=label,)

@admins.route('/application/')
def application():
    submit = db.session.query(Submit).all()
    return render_template('application.html', submit=submit,)


@admins.before_request
def loginsif():
    if session.get('username') == None:
        return redirect('/login')

# @admins.before_request
# def login_s():
#     print(session['username'])
#     return 123