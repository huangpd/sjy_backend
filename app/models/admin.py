from flask import session
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Admins(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(100))  # uid
    username = db.Column(db.String(100))  # 用户名
    password = db.Column(db.String(100))  # 密码
    time = db.Column(db.DateTime)  # 文件类型
    status = db.Column(db.String(20), default='1')  # 文件状态
    grade = db.Column(db.Integer)  # 用户等级
    texts = db.Column(db.Text, nullable=True)  # 备注


class Adminimg(db.Model):
    __tablename__ = 'adminimg'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))  # uid
    uid = db.Column(db.String(100))  # uid
    url = db.Column(db.String(200))  # uid
    a = db.Column(db.String(200), default='#')  # uid
    grade = db.Column(db.Integer)  # 用户等级


class Sjyimg(db.Model):
    __tablename__ = 'sjyimg'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))  # uid
    uid = db.Column(db.String(100))  # uid
    url = db.Column(db.String(200))  # uid
    grade = db.Column(db.Integer)  # 用户等级


class Plateico(db.Model):
    __tablename__ = 'plateico'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ico = db.Column(db.String(200))  # ico
    name = db.Column(db.String(100))  # ico
    text = db.Column(db.String(100))  # ico
    url = db.Column(db.String(100))  # ico


class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(100), unique=True, index=True)  # 文件类型
    xy = db.Column(db.String(200))  # 文件名
    region = db.Column(db.String(200))  # 文件名
    base_url = db.relationship('Base', backref='region')

    def to_json(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'xy': self.xy,
            'region': self.region,
        }


class Base(db.Model):
    __tablename__ = 'base'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(255))
    name = db.Column(db.String(255))
    text = db.Column(db.String(255))
    h3 = db.Column(db.String(255))
    a = db.Column(db.String(200), default='#')  # uid
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))

    def to_json(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'name': self.name,
            'text': self.text,
            'h3': self.h3,
            'a': self.a,
            'region_id': self.region_id,
        }


class Submit(db.Model):
    __tablename__ = 'submit'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(255))
    gp = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    times = db.Column(db.DateTime)
    username = db.Column(db.String(255))
    base_name = db.Column(db.String(255))
    base_uid = db.Column(db.String(255))
    delete = db.Column(db.Integer, default=1)
    status = db.Column(db.Integer, default=0)


# 文章板块
#     标签板块
class Label(db.Model):
    __tablename__ = 'label'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(255))
    value = db.Column(db.String(255))
    article_url = db.relationship('Article', backref='label')
    # 文章表


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(255))
    title = db.Column(db.String(255))
    tt = db.Column(db.String(255))
    img_url = db.Column(db.String(255))
    texts = db.Column(db.String(255))
    label_value = db.Column(db.String(255))
    label_uid = db.Column(db.String(255))
    date = db.Column(db.Date)
    html = db.Column(db.Text)
    grade = db.Column(db.Integer, default=0)  # 文章等级
    deletes = db.Column(db.Integer, default=1)  # 文章是否删除 1为未删除
    label_id = db.Column(db.Integer, db.ForeignKey('label.id'))


class Forms(db.Model):
    __tablename__ = 'forms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(255))
    times = db.Column(db.DateTime(255))
    demand = db.Column(db.String(255))
    company_genre = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    policy = db.Column(db.String(255))
    position = db.Column(db.String(255))
    taxes = db.Column(db.String(255))
    text = db.Column(db.String(255))
    status = db.Column(db.Integer, default=0)
    deletes = db.Column(db.Integer, default=1)  # 文章是否删除 1为未删除


# 数据库小镇系统表
class TownAdmin(db.Model):
    __tablename__ = 'town_admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(100))  # uid
    username = db.Column(db.String(100))  # 用户名
    password = db.Column(db.String(100))  # 密码
    time = db.Column(db.DateTime)  # 文件类型
    status = db.Column(db.String(20), default='1')  # 文件状态
    grade = db.Column(db.Integer)  # 用户等级
    texts = db.Column(db.Text, nullable=True)  # 备注


class Town(db.Model):
    __tablename__ = 'town'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(100))  # uid
    name = db.Column(db.String(100))  # 小镇名字
    province = db.Column(db.String(100))  # 省
    city = db.Column(db.String(100))  # 市
    area = db.Column(db.String(20), default='1')  # 区


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(100))  # uid
    company_name = db.Column(db.String(100))  # 公司名字
    company_uid = db.Column(db.String(100))  # 统一代码
    company_town_uid = db.Column(db.String(100))  # 公司所在小镇
    company_town_name = db.Column(db.String(100))  # 公司所在小镇
    username = db.Column(db.String(255))   # 联系人
    phone = db.Column(db.String(255))  # 联系电话
    BelongOrg = db.Column(db.String(255))  # 登记机关
    OperName = db.Column(db.String(255))  # 法人名
    StartDate = db.Column(db.Date)  # 成立日期
    EndDate = db.Column(db.String(255))  # 吊销日期
    Status = db.Column(db.String(255))  # 企业状态
    Province = db.Column(db.String(255))  # 省份
    No = db.Column(db.String(255))  # 注册号
    RegistCapi = db.Column(db.String(255))  # 注册资本
    EconKind = db.Column(db.String(255))  # 企业类型
    Address = db.Column(db.String(255))  # 地址
    Scope = db.Column(db.String(255))  # 经营范围
    json_text = db.Column(db.Text)  # 全部json
    company_abnormal_amount = db.Column(db.Integer, default=0)
    company_court_notice_amount = db.Column(db.Integer, default=0)
    company_search_shiXin_amount = db.Column(db.Integer, default=0)
    company_abnormal = db.relationship("CompanyAbnormal", backref="company")
    company_court_notice = db.relationship("CompanyCourtNotice", backref="company")
    company_search_shiXin = db.relationship("CompanySearchShiXin", backref="company")


# 入驻公司异常信息表
class CompanyAbnormal(db.Model):
    __tablename__ = 'company_abnormal'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_uid = db.Column(db.String(100))  # 统一代码
    compauy_name = db.Column(db.String(100))  # 公司名字
    AddReason = db.Column(db.String(100))  # 列入经营异常名录原因
    AddDate = db.Column(db.DateTime)  # 列入日期
    RomoveReason = db.Column(db.String(100))  # 移出经营异常名录原因
    RemoveDate = db.Column(db.String(100))  # 移出日期
    DecisionOffice = db.Column(db.String(100))  # 作出决定机关
    RemoveDecisionOffice = db.Column(db.String(100))  # 移除决定机关
    status = db.Column(db.Integer, default=1)  # 状态
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))


# 查询开庭公告
class CompanyCourtNotice(db.Model):
    __tablename__ = 'company_court_notice'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Defendantlist = db.Column(db.String(100))  # 被告/被上诉人
    Executegov = db.Column(db.String(100))  # 法院
    Prosecutorlist = db.Column(db.String(100))  # 原告/上诉人
    LianDate = db.Column(db.String(100))  # 开庭日期
    CaseReason = db.Column(db.String(100))  # 案由
    nId = db.Column(db.String(100))  # 内部ID
    CaseNo = db.Column(db.String(100))  # 案号
    status = db.Column(db.Integer, default=1)  # 状态
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))


# 失信被执行人信息
class CompanySearchShiXin(db.Model):
    __tablename__ = 'company_search_shiXin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nid = db.Column(db.String(100))  # 内部主键
    Sourceid = db.Column(db.String(100))  # 官网主键（内部保留字段，一般为空）
    Uniqueno = db.Column(db.String(100))  # 唯一编号（内部保留字段，一般为空）
    Name = db.Column(db.String(100))  # 被执行人姓名/名称
    Liandate = db.Column(db.String(100))  # 立案时间
    Anno = db.Column(db.String(100))  # 案号
    Orgno = db.Column(db.String(100))  # 身份证号码/组织机构代码
    Ownername = db.Column(db.String(100))  # 法定代表人或者负责人姓名
    Executegov = db.Column(db.String(100))  # 执行法院
    Province = db.Column(db.String(100))  # 所在省份缩写
    Executeunite = db.Column(db.String(100))  # 做出执行依据单位
    Yiwu = db.Column(db.String(100))  # 生效法律文书确定的义务
    Executestatus = db.Column(db.String(100))  # 被执行人的履行情况
    Actionremark = db.Column(db.String(100))  # 失信被执行人行为具体情形
    Publicdate = db.Column(db.String(100))  # 发布时间
    Age = db.Column(db.String(100))  # 年龄
    Sexy = db.Column(db.String(100))  # 性别
    Updatedate = db.Column(db.String(100))  # 数据更新时间（内部保留字段，现已不再更新时间）
    Executeno = db.Column(db.String(100))  # 执行依据文号
    Performedpart = db.Column(db.String(100))  # 已履行
    Unperformpart = db.Column(db.String(100))  # 未履行
    OrgType = db.Column(db.String(100))  # 组织类型（1：自然人，2：企业，3：社会组织，空白：无法判定）
    OrgTypeName = db.Column(db.String(100))  # 组织类型名称
    status = db.Column(db.Integer, default=1)  # 状态
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))


# 公司股东信息
class CompanyPartner(db.Model):
    __tablename__ = 'company_partner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StockName = db.Column(db.String(100))  # 股东
    StockType = db.Column(db.String(100))  # 股东类型
    StockPercent = db.Column(db.String(100))  # 出资比例
    ShouldCapi = db.Column(db.String(100))  # 认缴出资额
    ShoudDate = db.Column(db.String(100))  # 认缴出资时间
    InvestType = db.Column(db.String(100))  # 认缴出资方式
    InvestName = db.Column(db.String(100))  # 实际出资方式
    RealCapi = db.Column(db.String(100))  # 实际出资额
    CapiDate = db.Column(db.String(100))  # 实缴时间

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))


# 公司工商变更信息
class CompanyChange(db.Model):
    __tablename__ = 'company_change'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProjectName = db.Column(db.String(100))  # 变更事项
    BeforeContent = db.Column(db.String(100))  # 变更前内容
    AfterContent = db.Column(db.String(100))  # 变更后内容
    ChangeDate = db.Column(db.String(100))  # 变更日期

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))




class RefreshTime(db.Model):
    __tablename__ = 'refresh_time'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    times = db.Column(db.String(100))  # 刷新时间