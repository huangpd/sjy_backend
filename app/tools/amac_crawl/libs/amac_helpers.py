import requests
import random
import json
from .models import mongo_db
from lxml import etree

headers = {
    'Content-Type': 'application/json',
    'Referer': 'http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}


class AmacCrawl:
    def __init__(self, round=None):
        self.round = round

    def get_r_json(self, url):
        attempts = 0
        success = False
        while attempts < 10 and not success:
            try:
                r = requests.post(url, data=json.dumps({}), headers=headers)
                r_json = json.loads(r.text)
                if len(r_json) > 0:
                    success = True
            except:
                attempts += 1
                print("Retry-{attempt}".format(attempt=attempts))
                if attempts == 10:
                    break
        return r_json

    def manager_total_count(self):
        url = "http://gs.amac.org.cn/amac-infodisc/api/pof/manager?page=0&size=20"
        r_json = self.get_r_json(url)
        totalElements = int(r_json["totalElements"])
        return int(totalElements)

    def product_total_count(self):
        url = "http://gs.amac.org.cn/amac-infodisc/api/pof/fund?page=0&size=20"
        r_json = self.get_r_json(url)
        totalElements = int(r_json["totalElements"])
        return int(totalElements)

    def manager_url_list(self):
        url = "http://gs.amac.org.cn/amac-infodisc/api/pof/manager?page=0&size=20"
        r_json = self.get_r_json(url)
        total_pages = int(r_json["totalPages"])
        url_list = []
        for x in range(0, total_pages):
            size = 20
            rand_val = random.random()
            url = "http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=" \
                  + str(rand_val) + "&page=" + str(x) + "&size=" + str(size)
            url_list.append(url)
        return url_list

    def product_url_list(self):
        url = "http://gs.amac.org.cn/amac-infodisc/api/pof/fund?page=0&size=20"
        r_json = self.get_r_json(url)
        total_pages = int(r_json["totalPages"])
        url_list = []
        for x in range(0, total_pages):
            size = 20
            rand_val = random.random()
            url = "http://gs.amac.org.cn/amac-infodisc/api/pof/fund?rand=" \
                  + str(rand_val) + "&page=" + str(x) + "&size=" + str(size)
            url_list.append(url)
        return url_list

    def m_save_to_mongo(self, url):
        r_json = self.get_r_json(url)
        msg_list = []
        if 'content' in r_json:
            for data_item in r_json['content']:
                data_item['round'] = self.round
                data_item['managerName'] = data_item['managerName'].replace("（", "(").replace("）", ")")
                manager = mongo_db.amac_managers.find_one({'url': data_item['url']})
                if manager:
                    mongo_db.amac_managers.update_one({'_id': manager['_id']}, {"$set": data_item}, upsert=False)
                    msg_list.append("update {}".format(data_item['managerName']))
                else:
                    mongo_db.amac_managers.insert_one(data_item)
                    msg_list.append("insert {}".format(data_item['managerName']))
        return msg_list

    def p_save_to_mongo(self, url):
        r_json = self.get_r_json(url)
        msg_list = []
        if 'content' in r_json:
            for data_item in r_json['content']:
                data_item['round'] = self.round
                data_item['managerName'] = data_item['managerName'].replace("（", "(").replace("）", ")")
                data_item['fundName'] = data_item['fundName'].replace("（", "(").replace("）", ")")
                product = mongo_db.amac_products.find_one({'url': data_item['url']})
                if product:
                    data_item['manager_id'] = product['manager_id']
                    mongo_db.amac_products.update_one({'_id': product['_id']}, {"$set": data_item}, upsert=False)
                    msg_list.append("update {}".format(data_item['fundName']))
                else:
                    manager = mongo_db.amac_managers.find_one({'url': data_item['managerUrl'][11:]})
                    if manager:
                        data_item['manager_id'] = str(manager['_id'])
                    mongo_db.amac_products.insert_one(data_item)
                    msg_list.append("insert {}".format(data_item['fundName']))
        return msg_list


def get_manager_detail(rq_url):
    data_item = {}
    response = requests.get(rq_url, timeout=2)
    if response.status_code == 200:
        html_doc = response.content.decode("utf-8")
        tree = etree.HTML(html_doc)
        is_third_party = tree.xpath("//td[contains(string(), '是否为符合提供投资建议条件的第三方机构:')]/following-sibling::td/text()")
        if len(is_third_party) > 0:
            is_third_party = is_third_party[0].strip()
            if is_third_party == '是':
                data_item['is_third_party'] = is_third_party
        is_member = tree.xpath("//td[contains(string(), '是否为会员:')]/following-sibling::td/text()")[0].strip()
        data_item['is_member'] = is_member
        if is_member == '是':
            member_item = {}
            member_item['type'] = tree.xpath("//td[contains(string(), '当前会员类型:')]/following-sibling::td/text()")[
                0].strip()
            member_item['join_date'] = tree.xpath("//td[contains(string(), '入会时间:')]/following-sibling::td/text()")[
                0].strip()
            data_item['member_item'] = member_item
        law_status = tree.xpath("//td[contains(string(), '法律意见书状态:')]/following-sibling::td/text()")[0].strip()
        if law_status == '办结':
            law_station = tree.xpath("//td[contains(string(), '律师事务所名称:')]/following-sibling::td/text()")
            if len(law_station) > 0:
                law_station = law_station[0].strip()
                data_item['law_station'] = law_station
            lawyers = tree.xpath("//td[contains(string(), '律师姓名:')]/following-sibling::td/text()")
            if len(lawyers) > 0:
                lawyers = lawyers[0].strip()
                lawyer_list = lawyers.split(',')
                data_item['lawyer_list'] = lawyer_list
        return data_item


def get_product_detail(rq_url):
    data_item = {}
    response = requests.get(rq_url, timeout=2)
    if response.status_code == 200:
        html_doc = response.content.decode("utf-8")
        tree = etree.HTML(html_doc)
        fund_type = tree.xpath("//td[contains(string(), '基金类型:')]/following-sibling::td/text()")[0].strip()
        if fund_type:
            data_item['fund_type'] = fund_type
        manage_type = tree.xpath("//td[contains(string(), '管理类型:')]/following-sibling::td/text()")[0].strip()
        if manage_type:
            data_item['manage_type'] = manage_type
        work_status = tree.xpath("//td[contains(string(), '运作状态:')]/following-sibling::td/text()")[0].strip()
        if work_status:
            data_item['work_status'] = work_status
    return data_item    
    