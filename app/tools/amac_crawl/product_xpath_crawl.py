from libs.amac_helpers import get_product_detail
from libs.models import mongo_db
import threading
import pendulum

products = list(mongo_db.amac_products.find({}, {'url': 1}))


class ManagerThread(threading.Thread):
    def __init__(self, sid):
        threading.Thread.__init__(self)
        self.sid = sid

    def run(self):
        while len(products) > 0:
            try:
                url = products.pop()['url']
                rq_url = "http://gs.amac.org.cn/amac-infodisc/res/pof/fund/{}".format(url)
                data_item = get_product_detail(rq_url)
                mongo_db.amac_products.update_one(
                    {'url': url}, {'$set': data_item}, upsert=False)
                print(data_item)
            except:
                continue


def add_log(msg):
    logging = "{} - {} \n".format(pendulum.now(
        'Asia/Shanghai').to_datetime_string(), msg)
    with open("./amac_log.txt", "a") as f:
        f.write(logging)


add_log("-" * 20)
add_log("开始爬取私募产品详情")
threads = []
for i in range(1, 30):
    t = ManagerThread(i)
    threads.append(t)
    t.start()
for t in threads:
    t.join()
print("Done")
add_log("结束")
add_log("-" * 20)
