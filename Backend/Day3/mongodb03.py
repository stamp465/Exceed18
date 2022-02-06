from shelve import BsdDbShelf
from pymongo import MongoClient

from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()

myclient = MongoClient('mongodb://localhost', 27018)
db = myclient["stamp01"]
collection = db["user"]

class Data(BaseModel):
    name : str
    roll_no : int
    branch : str


@app.get("/data/all")
def get_all_data():
    result = collection.find({},{"_id":0})
    dic = []
    for r in result:
        print(r)
        dic.append(r)
    return dic

@app.get("/data/{name}")
def get_name_data(name:str):
    result = collection.find_one({"name":name},{"_id":0})
    if result != None :
        return {
            "result" : "done",
            "result" : result
        }
    else :
        raise HTTPException(404, f"Not found {name}")

@app.post("/data/add")
def add_new_data(data: Data):
    a = jsonable_encoder(data)
    print(a)
    collection.insert_one(a)
    return {
        "result" : "done"
    }















