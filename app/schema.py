# build a schema using pydantic
from pydantic import BaseModel

class ReferenceLetterRequest(BaseModel):
    name: str
    description: str

class Student(BaseModel):
    name:str
    email:str
    school_id:int

    class Config:
        orm_mode = True

class Teacher(BaseModel):
    name:str
    email:str
    degree:str

    class Config:
        orm_mode = True