from pymongo import MongoClient 
  
# Making Connection
myclient = MongoClient('mongodb://localhost', 27018)

# database 
db = myclient["stamp01"]
collection = db["user"]
print(myclient.list_database_names())

'''
# insert 
data = {
    "name" : "Orange",
    "price" : 40
}
collection.insert_one(data)

mylist = [
  { "_id": 1, "name": "Vishwash", "Roll No": "1001", "Branch":"CSE"},
  { "_id": 2, "name": "Vishesh", "Roll No": "1002", "Branch":"IT"},
  { "_id": 3, "name": "Shivam", "Roll No": "1003", "Branch":"ME"},
  { "_id": 4, "name": "Yash", "Roll No": "1004", "Branch":"ECE"},
]
x = collection.insert_many(mylist)
print(x.inserted_ids)


#find 
mycol = db["user"]
for x in mycol.find():
    print(x)
for x in mycol.find({}, {"_id":0, "name": 1, "Branch": 1 }):
    print(x)



# query
mycol = db["user"]
myquery = {  "Branch": "IT" }
mydoc = mycol.find(myquery,{"_id":0, "name": 1, "Roll No": 1})
for x in mydoc:
  print(x)

mycol = db["user"]
myquery = { "name": { "$gt": "V" } , 'Roll No': { "$gt": '1001' } }
mydoc = mycol.find(myquery,{"_id":0, "name": 1, "Roll No": 1})
for x in mydoc:
  print(x)


#delete
mycol = db["user"]
myquery = { "name": "Vishwash" }
#mycol.delete_one(myquery)

x = mycol.delete_many(myquery)
print(x.deleted_count, " documents deleted.")


# update
mycol = db["user"]
myquery = { "name": "Shivam" }
newvalues = { "$set": { "name": "Shivam NEWWW" } }
mycol.update_one(myquery, newvalues)

mycol = db["user"]
myquery = { "name": "Shivam NEWWW" }
newvalues = { "$set": { "name": "Shivam"} }
x = mycol.update_many(myquery, newvalues)
'''




















