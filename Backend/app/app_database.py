from pymongo import MongoClient

myclient = MongoClient('mongodb://localhost', 27017)

db = myclient["cafe"]

Cafe = db["cafe_data"]
Cafe_q = db["cafe_queue"]
Cafe_sit = db["cafe_sit"]
Queue = db["queue"]
Sensor = db["sensor"]