from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

student = {
    1234 : {
        "name" : "witnapat",
        "age" : 20
    }
    
}

class Item(BaseModel):
    name : str
    price : float
    discount : Optional[float]
    

@app.get("/")
def root():
    return {"Hello" : "Student"}

@app.get("/student/all")
def student_all():
    return {
        "student" : student
    }

@app.get("/student/find/{std_id}")
def student_find(std_id : int):
    return {
        "std_id" : std_id,
        "data" : student[std_id]
    }

@app.post("/student/add/{std_id},{name}")
def student_find(std_id : int, name : str, age: Optional[int] = None):
    student[std_id] = {
        "name" : name,
        "age" : age
    }
    return{
        "Add" : std_id
    }

