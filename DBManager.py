from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client.GapLogTest
log = db.Log

