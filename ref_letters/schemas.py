from lib2to3.pgen2.token import OP
from pydantic import BaseModel
from typing import Optional

class ReferenceLetterRequest(BaseModel):
    id: int
    name: str
    is_approved: Optional[bool] = None
    is_declined: Optional[bool] = None
    is_pending: Optional[bool] = None

class Student(BaseModel):
    id: int
    name: str
    school_id: int
    email: str

class Teacher(BaseModel):
    id: int
    name: str
    email: str

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str