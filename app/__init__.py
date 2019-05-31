from flask import Flask
from app.web.index import web
from app.townss.index import townss
from app.admin.admins import admins
from app.survey.survey import survey
from app.login.logins import logins
from app.models.admin import db
# from app.models.book import db
def create_app():
    app = Flask(__name__,)
    # 引入Flask框架

    app.jinja_env.variable_start_string = '{{ '
    app.jinja_env.variable_end_string = ' }}'
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    #装载配置文件
    # register_blueprint(app)



    db.init_app(app)
    db.create_all(app=app)#映射到数据库
    #关联插件 插件用作数据库操作


    register_blueprint(app) #蓝图注册
    townss_blueprint(app) #蓝图注册
    survey_blueprint(app) #蓝图注册
    admin_blueprint(app) #蓝图注册
    logins_blueprint(app) #蓝图注册
    return app


#蓝图注册

def townss_blueprint(app):
    app.register_blueprint(townss)

def register_blueprint(app):
    app.register_blueprint(web)

def admin_blueprint(app):
    app.register_blueprint(admins)

def logins_blueprint(app):
    app.register_blueprint(logins)

def survey_blueprint(app):
    app.register_blueprint(survey)



