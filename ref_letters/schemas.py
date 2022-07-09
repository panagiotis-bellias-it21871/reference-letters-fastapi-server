from lib2to3.pgen2.token import OP
from typing import Optional

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from pydantic import BaseModel


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

class User(SQLAlchemyBaseUserTableUUID, BaseModel):
    username: str
    email: str
    full_name: str
    student: bool
    teacher: bool
    admin: bool
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str
