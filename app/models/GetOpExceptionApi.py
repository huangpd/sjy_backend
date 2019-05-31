import requests
from app.models.ApiEntrance import Api
class GetOpException:
    # key = '669fe09a7a3046358a71fbfc29a24935'
    key = '33f099c2e2e84004a86619dd09ce1ee5'
    url = 'http://api.qichacha.com/ECIException/GetOpException?key=' + key + '&keyNo={}'
    # screat_key = '9DB60CB7EBB3E6B164BD62A1C41F8298'
    screat_key = 'B7F25719F5413AD697468B24E033EC29'

    @classmethod
    def get_details_by_name(cls, keyword):
        url = cls.url.format(keyword)
        print(url)
        r = requests.get(url, headers=Api.get_headers(cls.key, cls.screat_key))
        if r.status_code == 200:
            return r.json()
        else:
            return {}

