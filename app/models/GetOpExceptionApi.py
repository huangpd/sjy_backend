import requests
from app.models.ApiEntrance import Api
class GetOpException:
    key = '669fe09a7a3046358a71fbfc29a24935'
    url = 'http://api.qichacha.com/ECIException/GetOpException?key=' + key + '&keyNo={}'
    screat_key = '9DB60CB7EBB3E6B164BD62A1C41F8298'

    @classmethod
    def get_details_by_name(cls, keyword):
        url = cls.url.format(keyword)
        print(url)
        r = requests.get(url, headers=Api.get_headers(cls.key, cls.screat_key))
        if r.status_code == 200:
            return r.json()
        else:
            return {}

