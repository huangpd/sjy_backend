import shutil
import string
from datetime import datetime
import os
import random
import time

import xlrd
from flask import request, jsonify, make_response, send_file
import json

from pypinyin import lazy_pinyin
from werkzeug.utils import secure_filename

from app.models.GetOpExceptionApi import GetOpException
from app.models.admin import db, Town, Company, RefreshTime, CompanyAbnormal, CompanyCourtNotice, CompanySearchShiXin
from app.models.QichachaApi import Qichacha
from app.tools.FileExport import excel
from secure import mondb
from tools.datetime_to_json import DateEncoder
from . import townss
from sqlalchemy import extract, and_, or_


# **************** 小镇 ************************
# 添加小镇
@townss.route('/town_add/', methods=['POST'])
def town_add():
    if request.method == 'POST':
        name = request.form['name']
        province = request.form['address[province]']
        city = request.form['address[city]']
        area = request.form['address[area]']

        times = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        uid = str(random.randint(1000, 9999))  # str用于把数字转换成字符串
        uid = 'town' + times + uid

        role = Town(uid=uid, name=name, province=province, city=city, area=area)
        db.session.add(role)
        db.session.commit()
        t = {
            'uid': role.uid,
            'name': role.name,
            'province': role.province,
            'city': role.city,
            'area': role.area,
        }

        data = jsonify(t)
        return data, 200, {"ContentType": "application/json"}


# 删除小镇
@townss.route('/town_delete/', methods=['POST'])
def town_delete():
    if request.method == 'POST':
        uid = request.form['uid']
        label = db.session.query(Town).filter(Town.uid == uid).first()
        db.session.delete(label)
        db.session.commit()

        user1 = {"value": 1, "message": '数据彻底删除！'}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}


# 所有小镇
@townss.route('/town_message/', methods=['POST'])
def town_message():
    if request.method == 'POST':
        towns = db.session.query(Town).all()
        towns = town_josn(towns)
        data = json.dumps(towns)
        return data, 200, {"ContentType": "application/json"}


# 小镇数据分类展示
@townss.route('/town_message_date/', methods=['POST'])
def town_message_date():
    if request.method == 'POST':
        town = db.session.query(Town).all()
        company = db.session.query(Company).all()
        towns = []
        town_t = []
        for i in town:
            company_amount = 0
            for y in company:
                if i.uid == y.company_town_uid:
                    company_amount = company_amount + 1
            ss = i.province
            ss = ss.strip('省')
            ss = ss.strip('市')
            if town_t.count(ss) == 0:
                town_t.append(ss)
                towny = {
                    '位置': ss,
                    '私募公司数量': company_amount
                }
                towns.append(towny)
            else:
                for x in towns:
                    if x['位置'] == ss:
                        x['私募公司数量'] = x['私募公司数量'] + company_amount
        data = {
            'value': 1,
            'message': towns,
        }
        data = jsonify(data)
        return data, 200, {"ContentType": "application/json"}


def town_josn(v):
    y = []
    for i in v:
        y.append({'id': i.id, 'uid': i.uid, 'name': i.name, 'province': i.province, 'city': i.city, 'area': i.area, })
    return y


# ****************** 公司 ************************
# 添加公司
@townss.route('/company_add/', methods=['POST'])
def company_add():
    if request.method == 'POST':
        company_name = request.form['company_name']
        company_uid = request.form['company_uid']
        company_town_uid = request.form['company_town_uid']
        company_town_name = request.form['company_town_name']
        username = request.form['username']
        phone = request.form['phone']

        company = db.session.query(Company).all()

        v = True
        for x in company:

            x_company_uid = x.company_uid
            x_company_uid = x_company_uid.strip()
            company_uid = company_uid.strip()

            if x_company_uid == company_uid:
                v = False

        if v == False:
            data = {
                'value': 2,
                'message': '公司已经提交了，请不要重新提交',
            }
            data = jsonify(data)
            return data, 200, {"ContentType": "application/json"}

        times = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        uid = str(random.randint(1000, 9999))  # str用于把数字转换成字符串
        uid = 'company' + times + uid

        company_json = Qichacha.get_details_by_name(company_uid)
        company_json = company_json['Result']

        role = Company(uid=uid, company_name=company_name, company_uid=company_uid, company_town_name=company_town_name,
                       company_town_uid=company_town_uid, username=username, phone=phone,
                       BelongOrg=company_json['BelongOrg'], OperName=company_json['OperName'],
                       StartDate=company_json['StartDate'], EndDate=company_json['EndDate'],
                       Status=company_json['Status'], Province=company_json['Province'], No=company_json['No'],
                       RegistCapi=company_json['RegistCapi'], EconKind=company_json['EconKind'],
                       Address=company_json['Address'], Scope=company_json['Scope'], json_text=json.dumps(company_json))

        db.session.add(role)
        db.session.commit()
        t = {
            'uid': role.uid,
            'company_name': role.company_name,
            'company_uid': role.company_uid,
            'company_town_uid': role.company_town_uid,
            'company_town_name': role.company_town_name,
            'username': role.username,
            'phone': role.phone,
        }

        data = {
            'value': 1,
            'message': t,
        }
        data = jsonify(data)
        return data, 200, {"ContentType": "application/json"}


# 根据xls导入公司
@townss.route('/xls/', methods=['POST'])
def xls():
    ff = request.files['file']
    filesname = "".join(lazy_pinyin(ff.filename))
    d = os.path.dirname(__file__)
    basepath = os.path.dirname(d)
    upload_path = os.path.join(basepath, '../dist/xls', secure_filename(filesname))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
    ff.save(upload_path)
    data = open_excel(upload_path).sheets()[0]
    table = data.nrows
    towns = db.session.query(Town).all()
    company = db.session.query(Company).all()
    objects = []
    for i in range(1, table):
        datas = data.row(i)
        times = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        uid = str(random.randint(1000, 9999))  # str用于把数字转换成字符串
        uid = 'company' + times + uid
        town_name = datas[3].value

        v = True
        for x in company:
            x_company_uid = x.company_uid
            x_company_uid = x_company_uid.strip()
            company_uid = datas[1].value
            company_uid = company_uid.strip()
            if x_company_uid == company_uid:
                v = False
        if v == True:
            company_town_uid = ''
            company_town_name = ''
            for y in towns:
                if y.name == town_name:
                    company_town_uid = y.uid
                    company_town_name = y.name
            keyword = datas[1].value
            company_json = Qichacha.get_details_by_name(keyword)
            company_json = company_json['Result']
            if company_json['Result'] != None:
                role = Company(uid=uid, company_name=datas[0].value, company_uid=datas[1].value,
                               company_town_name=company_town_name, company_town_uid=company_town_uid,
                               username=datas[4].value, phone=datas[5].value, BelongOrg=company_json['BelongOrg'],
                               OperName=company_json['OperName'], StartDate=company_json['StartDate'],
                               EndDate=company_json['EndDate'], Status=company_json['Status'],
                               Province=company_json['Province'], No=company_json['No'],
                               RegistCapi=company_json['RegistCapi'], EconKind=company_json['EconKind'],
                               Address=company_json['Address'], Scope=company_json['Scope'],
                               json_text=json.dumps(company_json))
                objects.append(role)

    db.session.add_all(objects)
    db.session.commit()
    # return data
    user1 = {"value": 1, "message": '数据添加成功！'}
    data = json.dumps(user1)
    return data, 200, {"ContentType": "application/json"}


def open_excel(file):
    try:
        data = xlrd.open_workbook(file, encoding_override="utf-8")
        return data
    except Exception as e:
        print(str(e))


# 删除公司
@townss.route('/company_delete/', methods=['POST'])
def company_delete():
    if request.method == 'POST':
        uid = request.form['uid']
        label = db.session.query(Company).filter(Company.uid == uid).first()
        db.session.delete(label)
        db.session.commit()
        user1 = {"value": 1, "message": '数据彻底删除！'}
        data = json.dumps(user1)
        return data, 200, {"ContentType": "application/json"}


# 修改公司
@townss.route('/company_amend/', methods=['POST'])
def company_amend():
    if request.method == 'POST':
        uid = request.form['uid']

        company_name = request.form['company_name']
        company_uid = request.form['company_uid']
        company_town_uid = request.form['company_town_uid']
        company_town_name = request.form['company_town_name']
        username = request.form['username']
        phone = request.form['phone']

        label = db.session.query(Company).filter(Company.uid == uid).first()
        if label:
            label.company_name = company_name
            label.company_uid = company_uid
            label.company_town_uid = company_town_uid
            label.company_town_name = company_town_name
            label.username = username
            label.phone = phone
            db.session.commit()
            user1 = {"value": 1, "message": '数据修改成功！'}
            data = json.dumps(user1)
            return data, 200, {"ContentType": "application/json"}
        else:
            user1 = {"value": 0, "message": '没有找到记录！'}
            data = json.dumps(user1)
            return data, 200, {"ContentType": "application/json"}


# 加载所有公司
@townss.route('/company_message/', methods=['POST'])
def company_message():
    if request.method == 'POST':
        companys = db.session.query(Company).all()
        companys = company_josn(companys)
        data = json.dumps(companys)
        return data, 200, {"ContentType": "application/json"}


# 加载的公司字段
def company_josn(v):
    y = []
    for i in v:
        y.append({'id': i.id, 'uid': i.uid, 'company_name': i.company_name, 'company_uid': i.company_uid,
                  'company_town_uid': i.company_town_uid, 'company_town_name': i.company_town_name,
                  'username': i.username, 'phone': i.phone, })
    return y


# 导出excel的字段
def companys_export(companys):
    comInfo_list = []
    for com in companys:
        comInfo_list.append((com.company_name, com.company_town_name, com.username, com.phone,
                             com.BelongOrg, com.OperName, com.StartDate, com.phone,
                             com.Status, com.Province, com.RegistCapi, com.EconKind,
                             com.Address, com.Scope, com.company_abnormal_amount, com.company_court_notice_amount,
                             com.company_search_shiXin_amount))
    return comInfo_list


# 动态加载公司
@townss.route('/company_message_v/', methods=['POST'])
def company_message_v():
    if request.method == 'POST':
        form = request.form
        province = form['province']
        city = form['city']
        area = form['area']
        is_export = int(form['is_export'])
        companys = db.session.query(Company).filter(Town.uid == Company.company_town_uid)
        if province == '全部':
            pass
        elif city == '全部':
            companys = companys.filter(Town.province == province)
        elif area == '全部':
            companys = companys.filter(Town.province == province, Town.city == city)
        else:
            companys = companys.filter(Town.province == province, Town.city == city, Town.area == area)
        companys = companys.all()
        if is_export:
            companys = companys_export(companys)
            columns = ['公司名称', '所属设基院', '联系人', '联系人电话', '监管局', 'opername', 'start-date', 'EndDate', '经营状态',
                       'province',
                       '注册资本', '公司类型', '公司地址', 'scope', '异常信息', '开庭报告', '失信被执行人信息']
            dir_path = './app/static/temp'
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
            file_suffix = 'xlsx'  # excel文件格式
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            output = excel(file_suffix, columns, companys)
            filename = ''.join(
                random.choice(string.ascii_letters + string.digits) for _ in range(15)) + '.' + file_suffix
            with open(dir_path + '/' + filename, 'wb') as f:
                f.write(output)
            return filename
        else:
            companys = company_josn(companys)
        data = json.dumps(companys, cls=DateEncoder)  # 使用自定义的序列化气序列化date类型数据
        return data, 200, {"ContentType": "application/json"}


# 导出公司信息到excel
@townss.route('/company_message_export/<filename>/')
def company_message_export(filename):
    file = './static/temp/' + filename
    response = make_response(send_file(file))
    response.headers["Content-Disposition"] = "attachment;"
    return response


# 私募数据统计
@townss.route('/multi_count/', methods=['POST'])
def multi_count():
    multiCompany_amount = 0
    multiManager_amount = 0
    multiProduct_amount = 0
    multiCapital_size = 0

    multiPart_amount = 0
    multiDuty_amount = 0
    multiOther_amount = 0
    companys = db.session.query(Company.company_name, Company.RegistCapi, Company.EconKind).all()
    for com in companys:
        pro_col = mondb["amac_products"]
        man_col = mondb["amac_managers"]
        res1 = pro_col.find_one({"fundName": com[0]})
        res2 = man_col.find_one({"managerName": com[0]})
        if res1 or res2:
            capital = com[1].split('万元')[0].strip()
            if capital:
                multiCapital_size += int(capital)
            multiCompany_amount += 1
            multiProduct_amount += 1
            if com[2].find('有限合伙'):
                multiPart_amount += 1
            elif com[2].find('有限责任'):
                multiDuty_amount += 1
            else:
                multiOther_amount += 1
        if res2:
            multiManager_amount += 1
    data = {
        "multiCompany_amount": multiCompany_amount,
        "multiManager_amount": multiManager_amount,
        "multiProduct_amount": multiProduct_amount,
        "multiCapital_size": multiCapital_size,
        "multiPart_amount": multiPart_amount,
        "multiDuty_amount": multiDuty_amount,
        "multiOther_amount": multiOther_amount,
    }
    data = json.dumps(data)
    return data, 200, {"ContentType": "application/json"}


# 公司数据分类展示
@townss.route('/company_message_date/', methods=['POST'])
def company_message_date():
    if request.method == 'POST':
        form = request.form
        date_min = int(form['date_min'])
        date_max = int(form['date_max'])
        town = db.session.query(Town).all()
        address = []
        province = []
        provinces = form['province']
        if provinces and provinces != 'None':
            for m in town:
                if m.province == form['province']:
                    province.append(m)
            address = province
            if address == []:
                data = {
                    'value': 1,
                    'message': [],
                    'amount': 0
                }
                data = jsonify(data)
                return data, 200, {"ContentType": "application/json"}
        city = []
        citys = form['city']
        if citys and citys != 'None':
            for m in province:
                if m.city == form['city']:
                    city.append(m)
            address = city
        area = []
        areas = form['area']
        if areas and areas != 'None':
            for m in city:
                if m.area == form['area']:
                    area.append(m)
            address = area
        company_data = []
        amountk = 0
        enterCapital_size = 0
        part_amount = 0
        duty_amount = 0
        sum_amount = 0
        for i in range(0, date_max - date_min):
            for y in range(1, 13):
                data = i + date_min
                condition = and_(extract('year', Company.StartDate) == data,
                                 extract('month', Company.StartDate) == y)
                if address:
                    company_town_uid = None
                    for x in address:
                        company_town_uid = or_(Company.company_town_uid == x.uid, company_town_uid)
                    conditions = and_(company_town_uid)
                    companys = db.session.query(Company).filter(condition, conditions).all()
                    companys1 = db.session.query(Company).filter(condition, Company.EconKind.like('%有限合伙%'),
                                                                 conditions).all()
                    companys2 = db.session.query(Company).filter(condition, Company.EconKind.like('%有限责任%'),
                                                                 conditions).all()
                else:
                    companys = db.session.query(Company).filter(condition, ).all()
                    companys1 = db.session.query(Company).filter(condition, Company.EconKind.like('%有限合伙%')).all()
                    companys2 = db.session.query(Company).filter(condition, Company.EconKind.like('%有限责任%')).all()
                Capitals = db.session.query(Company.RegistCapi).all()
                for j in Capitals:
                    capital = j[0].split('万元')[0].strip()
                    if capital:
                        enterCapital_size += int(capital)
                company_data_y = {
                    '日期': str(data) + '年' + str(y) + '月',
                    '有限合伙': len(companys1),
                    '有限责任': len(companys2),
                    '总量': len(companys),
                }
                amountk = len(companys) + amountk
                if amountk == 0:
                    company_data = []
                else:
                    company_data.append(company_data_y)
        for k in company_data:
            sum_amount += k['总量']
            part_amount += k['有限合伙']
            duty_amount += k['有限责任']
        data = {
            'value': 1,
            'message': company_data,
            'sum_amount': sum_amount,
            'part_amount': part_amount,
            'duty_amount': duty_amount,
            'amount': amountk,
            'enterCapital_size': enterCapital_size,
        }
        data = jsonify(data)
        return data, 200, {"ContentType": "application/json"}


# ********************** 公司风险 ***********************
@townss.route('/company_risks/', methods=['POST'])
def company_risks():
    if request.method == 'POST':
        refreshtime = db.session.query(RefreshTime).first()
        date1 = time.strptime(refreshtime.times, '%Y-%m-%d')
        date2 = time.localtime()
        d1 = datetime(date1[0], date1[1], date1[2])
        d2 = datetime(date2[0], date2[1], date2[2])
        delta = d2 - d1
        delta = delta.days
        if delta >= 7:
            refreshtime.times = time.strftime('%Y-%m-%d', date2)
            db.session.commit()
            company_risk_update()

        company_list = db.session.query(Company).limit(2).all()
        m = company_risks_v(company_list)
        value = 0
        if len(m) > 0:
            value = 1
        data = {
            'value': value,
            'message': m,
        }
        data = jsonify(data)
        return data, 200, {"ContentType": "application/json"}


def company_risks_v(company_list):
    ca = db.session.query(CompanyAbnormal).all()
    ccn = db.session.query(CompanyCourtNotice).all()
    cssx = db.session.query(CompanySearchShiXin).all()

    company_risk_list = []
    for i in company_list:
        ca_amount = 0
        for y in ca:
            if y.company_id == i.id:
                ca_amount = ca_amount + 1

        ccn_amount = 0
        for y in ccn:
            if y.company_id == i.id:
                ccn_amount = ccn_amount + 1

        cssx_amount = 0
        for y in cssx:
            if y.company_id == i.id:
                cssx_amount = cssx_amount + 1

        if ca_amount != 0 or ccn_amount != 0 or cssx_amount != 0:
            data = {'uid': i.uid, 'company_name': i.company_name, 'company_uid': i.company_uid,
                    'company_abnormal_amount': ca_amount, 'company_court_notice_amount': ccn_amount,
                    'company_search_shiXin_amount': cssx_amount}
            company_risk_list.append(data)

    return company_risk_list


def company_risk_update():
    # ca = db.session.query(CompanyAbnormal).all() # 入驻公司异常信息表
    ccn = db.session.query(CompanyCourtNotice).all()  # 查询开庭公告
    cssx = db.session.query(CompanySearchShiXin).all()  # 失信被执行人信息
    company_list = db.session.query(Company).limit(10)  # 公司列表

    for i in company_list:  # 遍历每个公司
        g_list_v = GetOpException.get_details_by_name(i.company_uid)  # 每个公司获企查查 异常列表
        if g_list_v['Status'] == 200:
            g_list_v = g_list_v['Result']
            for y in g_list_v:
                mm = db.session.query(CompanyAbnormal).filter(CompanyAbnormal.company_uid == i.company_uid,
                                                              CompanyAbnormal.AddDate == g_list_v[
                                                                  'AddDate']).first()
                if not mm:
                    print('不存在')
                    friendship = CompanyAbnormal(company_uid=i.company_uid, AddReason=y.AddReason,
                                                 AddDate=y.AddDate,
                                                 RomoveReason=y.RomoveReason, RemoveDate=y.RemoveDate,
                                                 DecisionOffice=y.DecisionOffice,
                                                 RemoveDecisionOffice=y.RemoveDecisionOffice,
                                                 company_id=i.company_id)
                    db.session.add(friendship)
                else:
                    print('存在')
                    friendship = mm
                    friendship.AddReason = y.AddReason
                    friendship.AddDate = y.AddDate
                    friendship.RomoveReason = y.RomoveReason
                    friendship.RemoveDate = y.RemoveDate
                    friendship.DecisionOffice = y.DecisionOffice
                    friendship.RemoveDecisionOffice = y.RemoveDecisionOffice
                db.session.commit()

#
# def g_list(value):
#     g_list_v = GetOpException.get_details_by_name(value)
#     return g_list_v
#
# def g_verification(company_id, company_uid, g_list_v, ca):
#
#     amount = len(g_list_v)
#     g_list_add = []
#     for i in g_list_v:
#         m = False
#         for y in ca:
#             if y.company_id == company_uid and y.AddDate == i.AddDate:
#                 if y.status == 0:
#                     amount = amount-1
#             elif y.company_id == company_uid and y.AddDate != i.AddDate:
#                 m = True
#         if m:
#             g_list = CompanyAbnormal(company_uid=company_uid, AddReason=i.AddReason, AddDate=i.AddDate,
#                                      RomoveReason=i.RomoveReason, RemoveDate=i.RemoveDate,
#                                      DecisionOffice=i.DecisionOffice, RemoveDecisionOffice=i.RemoveDecisionOffice,
#                                      company_id=company_id)
#     g_list_add.append(g_list)
#
#     db.session.add_all(g_list_add)
#     db.session.commit()
#     return amount
#
# def sc_list(value):
#     sc_list_v = SearchCourtNotice.get_details_by_name(value)
#     return sc_list_v
#
# def ss_list(value):
#     ss_list_v = SearchShiXin.get_details_by_name(value)
#     return ss_list_v

# for i in company_list:
#     g_value = GetOpException.get_details_by_name(i.company_uid)
#     sc_value = SearchCourtNotice.get_details_by_name(i.company_uid)
#     ss_value = SearchShiXin.get_details_by_name(i.company_uid)
#
#
#     if g_value != {}:
#         g_list = []
#         for x in g_value:
#
#             for y in ca:
#                 if y.company_id != i.id and y.AddDate != x.AddDate:
#                     company_abnormal = CompanyAbnormal(company_uid=i.uid, compauy_name=i.company_name,
#                                                        AddReason=x.AddReason, AddDate=x.AddDate,
#                                                        RomoveReason=x.RomoveReason, RemoveDate=x.RemoveDate,
#                                                        DecisionOffice=x.DecisionOffice, RemoveDecisionOffice=x.RemoveDecisionOffice,
#                                                        company_id=i.id)
#                     g_list.append(company_abnormal)
#         company_risks_g = len(g_list)
#     else:
#         company_risks_g = 0
#
#     if sc_value != {}:
#         sc_list = []
#         for x in sc_value:
#             company_court_notice = CompanyCourtNotice(Defendantlist=x.Defendantlist, Executegov=x.Executegov, Prosecutorlist=x.Prosecutorlist, LianDate=x.LianDate, CaseReason=x.CaseReason, nId=x.nId, CaseNo=x.CaseNo, status=x.status, company_id=i.id)
#             sc_list.append(company_court_notice)
#         company_risks_sc = len(sc_list)
#     else:
#         company_risks_sc = 0
