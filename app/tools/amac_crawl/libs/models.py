from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017')
mongo_db = client.amac

# res1 = client.amac.amac_products.find()
# res2 = client.amac.amac_managers.find()
#
# for item in res1:
#     i = item
#     print(i)
#
# for item in res2:
#     i = item
#     print(i)
