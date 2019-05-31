import threading
import pendulum
from libs.amac_helpers import AmacCrawl

round = pendulum.now('Asia/Shanghai').int_timestamp
print(round)
amac_crawl = AmacCrawl(round)
m_url_list = amac_crawl.manager_url_list()


class ManagerThread(threading.Thread):
    def __init__(self, sid):
        threading.Thread.__init__(self)
        self.sid = sid

    def run(self):
        while len(m_url_list) > 0:
            try:
                url = m_url_list.pop()
                msg_list = amac_crawl.m_save_to_mongo(url)
                print(msg_list)
            except:
                continue


def add_log(msg):
    logging = "{} - {} \n".format(pendulum.now('Asia/Shanghai').to_datetime_string(), msg)
    with open("./amac_log.txt", "a") as f:
        f.write(logging)


add_log("-" * 20)
add_log("开始爬取私募管理人")
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
