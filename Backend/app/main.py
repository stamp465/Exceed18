# https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
from datetime import datetime, timedelta
import re
from typing import Optional
from jose import JWTError, jwt

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

import app_database as app_db
import app_schemas as app_sch
import app_password as app_pwd
import app_service as app_ser


ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


########################### user #############################

@app.get("/")
async def root():
    return 0

@app.get("/hello")
async def hello():
    return "WELCOME TO CAFE"

@app.get("/{cafe_name}/hello")
async def helloCa(cafe_name:str):
    return f"WELCOME TO {cafe_name}"

@app.post("/{cafe_name}/{cafe_code}/insertqueue")
def insert_queue(cafe_name:str,cafe_code:int,data:app_sch.WillQueueInDB):
    app_ser.check_matching(cafe_code,cafe_name)
    
    query = {"phone":data.phone , "cafe_code":cafe_code}
    result =  app_db.Queue.find_one(query,{"_id":0})
    r = app_db.Cafe_q.find_one({"cafe_code":cafe_code},{"_id":0})
    
    #print(query,result)
    if result == None :
        data2 = {
            "cafe_code": cafe_code,
            "name": data.name,
            "phone": data.phone,
            "willsit" : data.willsit,
            "queue_number":   app_ser.get_queuenumber(cafe_code) + 1 
        }
        app_db.Queue.insert_one(data2)
        #print(r)
        newvalues = {}
        if r["last_queue"] == 0 :
            newvalues = {"$set":{"now_queue":r["now_queue"]+1,"last_queue":r["last_queue"]+1}}
        else :
            newvalues = {"$set":{"last_queue":r["last_queue"]+1}}
        app_db.Cafe_q.update_one({"cafe_code":cafe_code},newvalues)
        
        return {
            "result" : "insert_queue done"
        }
    a = result["queue_number"]
    raise HTTPException( status_code = 406 , detail = { "msg" : f"Your phone already queue in Queue No.{a}" } )
    

@app.get("/{cafe_name}/{cafe_code}/countqueue")
async def get_queue(cafe_name:str,cafe_code:int):
    app_ser.check_matching(cafe_code,cafe_name)
    r = app_db.Cafe_q.find_one({"cafe_code":cafe_code},{"_id":0})
    if r == None :
        raise HTTPException (status_code = 404 , detail = {"msg" : "no cafe"})
    waitQ = r["last_queue"]-r["now_queue"]
    return {
        "now_queue" : r["now_queue"],
        "last_queue" : r["last_queue"] ,
        "wait_queue" : waitQ
    }

@app.get("/{cafe_name}/{cafe_code}/get_number_byphone")
async def get_number_byphone(cafe_name:str,cafe_code:int,phone:app_sch.Phone):
    app_ser.check_matching(cafe_code,cafe_name)
    query = {"phone":phone.number , "cafe_code":cafe_code}
    result =  app_db.Queue.find_one(query,{"_id":0})
    if result == None :
        raise HTTPException (status_code = 404 , detail = {"msg" : "no queue with this phone"})
    return result["queue_number"]

@app.get("/{cafe_name}/{cafe_code}/get_number_now_sit")
async def get_number_sit(cafe_name:str,cafe_code:int):
    app_ser.check_matching(cafe_code,cafe_name)
    query = {"cafe_code":cafe_code}
    result =  app_db.Cafe_sit.find_one(query,{"_id":0})
    if result == None :
        raise HTTPException (status_code = 404 , detail = {"msg" : "no cafe"})
    return {
        "now_sit" : result["now_sit"]
    }

@app.get("/{cafe_name}/{cafe_code}/get_number_sit")
async def get_number_sit(cafe_name:str,cafe_code:int):
    app_ser.check_matching(cafe_code,cafe_name)
    query = {"cafe_code":cafe_code}
    r =  app_db.Cafe_sit.find_one(query,{"_id":0})
    if r == None :
        raise HTTPException (status_code = 404 , detail = {"msg" : "no cafe"})
    return {
        "all_sit" : r["all_sit"],
        "now_sit" : r["now_sit"] ,
        "user_in" : r["user_in"] ,
        "user_out" : r["user_out"] 
    }


status_in = 0
status_out = 0
@app.post("/{cafe_name}/{cafe_code}/update")
async def update_in_out(cafe_name:str,cafe_code:int,updateuser:app_sch.UpUser):
    app_ser.check_matching(cafe_code,cafe_name)
    query = {"cafe_code":cafe_code}
    print(updateuser)
    print(updateuser.sensor_in)
    print(updateuser.sensor_out)
    
    r =  app_db.Cafe_sit.find_one(query,{"_id":0})
    if r == None :
        raise HTTPException (status_code = 404 , detail = {"msg" : "no cafe"})
    if updateuser.sensor_in == 1 and status_in == 0:
        status_in = 1
        newvalues = {"$set":{"now_sit":r["now_sit"]+1,"user_in":r["user_in"]+1}}
        app_db.Cafe_sit.update_one(query,newvalues)
    elif updateuser.sensor_in == 0 and status_in == 1:
        status_in = 0
        
    if updateuser.sensor_out == 1 and status_out == 0:
        status_out = 1
        newvalues = {"$set":{"now_sit":r["now_sit"]-1,"user_out":r["user_out"]+1}}
        app_db.Cafe_sit.update_one(query,newvalues)
    elif updateuser.sensor_out == 0 and status_out == 1:
        status_out = 0
    
    return {
        "result" : "update done"
    }

########################### for admin #############################

@app.post("/login", response_model=app_sch.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    users_db = app_ser.get_user_from_db()
    #print(users_db)
    user = app_ser.authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = app_ser.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=app_sch.User)     
async def read_users_me(current_user: app_sch.User = Depends(app_ser.get_current_user)):
    #print(current_user.cafe_code)
    return current_user


@app.get("/{cafe_name}/{cafe_code}/getqueue")
async def get_queue(cafe_name:str,cafe_code:int,current_user: app_sch.User = Depends(app_ser.get_current_user)):
    app_ser.check_matching(cafe_code,cafe_name)
    app_ser.check_auth_allow(cafe_code,cafe_name,current_user.cafe_code,current_user.cafe_name)
    print(current_user.cafe_name,current_user.cafe_code)
    #print(type(current_user.cafe_code))
    result = app_db.Queue.find({"cafe_code":cafe_code},{"_id":0})
    if result == None :
        raise HTTPException (status_code = 404 , detail = {"msg" : "no cafe "})
    lis = []
    for i in result :
        print(i)
        lis.append(i)
    return lis


@app.delete("/{cafe_name}/{cafe_code}/clearqueue")
async def clear_queue(cafe_name:str,cafe_code:int,current_user:app_sch.User = Depends(app_ser.get_current_user)):
    app_ser.check_matching(cafe_code,cafe_name)
    app_ser.check_auth_allow(cafe_code,cafe_name,current_user.cafe_code,current_user.cafe_name)
    query = {"cafe_code":cafe_code}
    re = app_db.Queue.find_one({"cafe_code":cafe_code})
    if re == None :
        raise HTTPException (status_code = 404 , detail = {"msg" : "no cafe "})
    app_db.Queue.delete_many(query)
    
    r = app_db.Cafe_q.find_one({"cafe_code":cafe_code})
    if r == None :
        raise HTTPException (status_code = 404 , detail = {"msg" : "no cafe"})
    query1 = {"cafe_code":cafe_code}
    newvalues = {"$set":{"now_queue":0,"last_queue":0}}
    app_db.Cafe_q.update_one(query1,newvalues)
    
    return {
        "result" : "done"
    }

@app.delete("/{cafe_name}/{cafe_code}/deletequeue/{queue_number}")
async def clear_queue(cafe_name:str,cafe_code:int,queue_number:str,current_user:app_sch.User = Depends(app_ser.get_current_user)):
    app_ser.check_matching(cafe_code,cafe_name)
    app_ser.check_auth_allow(cafe_code,cafe_name,current_user.cafe_code,current_user.cafe_name)
    re = app_db.Queue.find_one({"cafe_code":cafe_code,"queue_number":int(queue_number)})
    if re == None :
        raise HTTPException (status_code = 404 , detail = {"msg" : "no cafe or no queue_number"})
    r = app_db.Cafe_q.find_one({"cafe_code":cafe_code})
    if r == None :
        raise HTTPException (status_code = 404 , detail = {"msg" : "no cafe"})
    
    query = {"cafe_code":cafe_code,"queue_number":int(queue_number)}
    #print(query)
    app_db.Queue.delete_one(query)
    query1 = {"cafe_code":cafe_code}
    newvalues = {"$set":{"now_queue":r["now_queue"]+1}}
    app_db.Cafe_q.update_one(query1,newvalues)
    return{
        "result" : "done"
    }
