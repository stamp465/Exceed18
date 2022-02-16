# https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

import app_database as app_db
import app_schemas as app_sch
import app_password as app_pwd

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_from_db() :
    result = app_db.Cafe.find({},{"_id":0})
    #print(result)
    dic = {}
    for r in result:
        dic[ r['username'] ] = r
    return dic

def check_matching(code : int,name : str) :
    query = {"cafe_code":code}
    result = app_db.Cafe.find_one(query)
    #print(result)
    if result == None :
        raise HTTPException (status_code = 404 , detail = {"msg" : "no cafe "})
    if result["cafe_name"]==name :
        return True
    #print(result)
    raise HTTPException (status_code = 404 , detail = {"msg" : "no cafe "})

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return app_sch.UserInDB(**user_dict)

def get_queuenumber(cafe_code: int):
    result =  app_db.Cafe_q.find_one({"cafe_code":cafe_code},{"_id":0})
    #print("\n\n\ntest\n\n\n")
    #print(cafe_code,result)
    if result != None :
        #print(result["last_queue"])
        return result["last_queue"]
    raise HTTPException(404, f"Cafe Not found")
    
def check_auth_allow(cafe_code:int,cafe_name:str,user_cafe_code:int,user_cafe_name:str) :
    if ( user_cafe_code == cafe_code ) and  ( cafe_name == user_cafe_name ) :
        #print("xxxx")
        return True
    raise HTTPException(405, "Method Not Allowed")

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not app_pwd.verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #print(payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = app_sch.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    users_db = get_user_from_db()
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

