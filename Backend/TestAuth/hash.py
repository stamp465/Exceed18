from datetime import datetime, timedelta
from typing import Optional

from pymongo import MongoClient

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

myclient = MongoClient('mongodb://localhost', 27018)
db = myclient["cafe"]
collection = db["cafe_data"]

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

'''
@app.post("/dasfladnadlb/add")
def add_new_data(data: Data):
    a = jsonable_encoder(data)
    print(a)
    collection.insert_one(a)
    return {
        "result" : "done"
    }
'''