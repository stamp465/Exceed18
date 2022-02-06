from pymongo import MongoClient

from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()

myclient = MongoClient('mongodb://localhost', 27018)
db = myclient["stamp01"]
collection = db["user"]

@app.get("/data/all")
def get_all_data():
    result = collection.find({},{"_id":0})
    dic = []
    for r in result:
        print(r)
        dic.append(r)
    return dic

@app.post("/data/add/{name}/{Roll_No}/{Branch}")
def add_new_data(name: str,Roll_No : int, Branch:str):
    data = {
        "name" : name,
        "Roll No" : Roll_No,
        'Branch': Branch
    }
    collection.insert_one(data)
    return {
        "result" : "done"
    }
    
@app.delete("/data/delete/{name}")
def delete_data(name: str):
    data = {
        "name" : name
    }
    collection.delete_one(data)
    return {
        "result" : "done"
    }

@app.put("/data/update/{name}/{New_Branch}")
def update_data(name: str, New_Branch: str):
    myquery = { "name": name }
    newvalues = { "$set": { "Branch": New_Branch } }
    collection.update_one(myquery, newvalues)
    return {
        "result" : "done"
    }
















