from pydantic import BaseModel
from typing import Optional

from zmq import QUEUE

#token for auth
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

#user admin for auth
class User(BaseModel):
    username: str
    cafe_name: str
    cafe_code: int


class UserInDB(User):
    hashed_password: str
    
#queue
class QueueInDB(BaseModel):
    queue_number : int
    name : str
    phone : int
    cafe_code : int
    
class WillQueueInDB(BaseModel):
    name : str
    phone : int

    
#count queue in cafe
class CountQueue(BaseModel):
    cafe_code : int
    now_queue : int
    last_queue : int

#count people in cafe
class NumberSit(BaseModel):
    cafe_code : int
    all_sit : int
    user_in : int
    user_out : int
    now_sit : int
