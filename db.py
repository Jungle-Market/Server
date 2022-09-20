from http import client
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.dbjunglemarket

db.items.insert_one({"name": "picnic"})
