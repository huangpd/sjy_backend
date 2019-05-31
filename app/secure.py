# 配置文件
import pymongo

DEBUG = True

# SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://user:ningben$ningben@yue@192.168.199.88:3306/town'
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://myuser:Shejiyuan201%1@47.92.30.18:3306/town'
# SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://user:ningben$ningben@yue@localhost:3306/town'
SQLALCHEMY_TRACK_MODIFICATIONS = True
monclient = pymongo.MongoClient("mongodb://localhost:27017/")
mondb = monclient["amac"]

# 数据库类型 引用的包 账号 密码 地址 端口号 数据库名字 不能有空格


SECRET_KEY = 'fkdjsafjdkfdlkjfadskjfadskljdsfklj111111fkdjsafjdkfdlkjfadskjfadskljdsfklj111111'
# 数据加密的秘钥

PERMANENT_SESSION_LIFETIME=5*60*60