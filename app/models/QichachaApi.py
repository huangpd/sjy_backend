import requests
from app.models.ApiEntrance import Api
class Qichacha:
    # key = '669fe09a7a3046358a71fbfc29a24935'
    # screat_key = '9DB60CB7EBB3E6B164BD62A1C41F8298'
    key = '33f099c2e2e84004a86619dd09ce1ee5'
    screat_key = 'B7F25719F5413AD697468B24E033EC29'

    url = 'http://api.qichacha.com/ECIV4/GetDetailsByName?key='+key+'&dtype=json&keyword={}'


    @classmethod
    def get_details_by_name(cls, keyword):
        url = cls.url.format(keyword.strip())
        r = requests.get(url, headers=Api.get_headers(cls.key, cls.screat_key))
        print(r)
        if r.status_code == 200:
            return r.json()
        else:
            return {}






