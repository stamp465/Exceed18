from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    id : int
    name : str
    age : Optional[int]
    
students = {
    1 : {
        "id" : 152,
        "name" : "Witna"
    }
}

@app.get("/student/all")
def student_all():
    return students

@app.get("/student/all/{id}")
def student_get_id(id :int):
    return students[id].name

@app.post("/student/new")
def student_new(student : Student):
    students[student.id] = student
    return {
        "Add" : student.id
    }


