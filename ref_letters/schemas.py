from typing import List
from pydantic import BaseModel

class ReferenceLettersRequestBase(BaseModel):
    carrier_name: str
    carrier_email: str
    status: str
    text: str

class ReferenceLetterRequestCreate(ReferenceLettersRequestBase):
    teacher_id: int
    student_id: int

class ReferenceLetterRequest(ReferenceLettersRequestBase):
    id: int

    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    full_name: str
    school: str
    school_id: str
    grades_url: str
    user_username: str


class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    reference_letter_requests: List[ReferenceLetterRequest] = []

    class Config:
        orm_mode = True

class TeacherBase(BaseModel):
    full_name: str
    description: str
    user_username: str

class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    id: int
    reference_letter_requests: List[ReferenceLetterRequest] = []

    class Config:
        orm_mode = True
