from lib2to3.pgen2.token import OP
from pydantic import BaseModel
from typing import Optional

class ReferenceLetterRequest(BaseModel):
    id: int
    teacher_id: int
    student_id: int
    carrier_name: str
    carrier_email: str
    status: str
    text: str

class Student(BaseModel):
    id: int
    name: str
    email: str
    school: str
    school_id: str
    grades_url: str

class Teacher(BaseModel):
    id: int
    name: str
    email: str
    description: str

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str