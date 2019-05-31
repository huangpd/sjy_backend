import time
from hashlib import md5
class Api:
    @classmethod
    def get_time_tup(cls):
        time_tup = str(int(time.time()))
        return time_tup
    # md5加密
    @classmethod
    def set_md5(cls, s):
        new_md5 = md5()
        new_md5.update(s.encode(encoding='utf-8'))
        s_md5 = new_md5.hexdigest().upper()
        return s_md5
    # 设置请求头
    @classmethod
    def get_headers(cls, key, screat_key):
        headers = dict()
        token = key + cls.get_time_tup() + screat_key
        headers["Token"] = cls.set_md5(token)
        headers["Timespan"] = cls.get_time_tup()
        return headers