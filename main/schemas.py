# build a schema using pydantic
from typing import Optional
from pydantic import BaseModel

class ReferenceLetterRequestBase(BaseModel):
    name: "str"
    description: Optional[str] = None

class StudentBase(BaseModel):
    name: "str"
    email: "str"
    school_id: "int"

class TeacherBase(BaseModel):
    name: "str"
    email: "str"
    degree: "str"

class ReferenceLetterRequestCreate(ReferenceLetterRequestBase):
    pass

class StudentCreate(StudentBase):
    pass

class TeacherCreate(TeacherBase):
    pass

class ReferenceLetterRequest(ReferenceLetterRequestBase):
    id: int

    class Config:
        orm_mode = True

class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True

class Teacher(TeacherBase):
    id: int

    class Config:
        orm_mode = True