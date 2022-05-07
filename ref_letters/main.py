from fastapi import Depends, FastAPI

'''
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ref_letters.db import get_session, init_db
from ref_letters.models import ReferenceLetterRequest, ReferenceLetterRequestCreate, Student, StudentCreate, Teacher, TeacherCreate
'''
from .schemas import User #ReferenceLetterRequest
from .utils import get_current_user
#from .db import database

# YT1
from .schemas import fakedb_rl_requests, fakedb_students, fakedb_teachers, ReferenceLetterRequest, Student, Teacher

app = FastAPI()

'''
@app.on_event("startup")
async def on_startup():
    await database.connect()
    # await init_db()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
'''

@app.get("/")
def read_root():
    return {"greetings": "Welcome to FastAPI Python"}

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# YT1
#async
@app.get("/rl_requests") #, response_model=List[ReferenceLetterRequest])
def get_rl_requests():#session: AsyncSession = Depends(get_session)):
    return fakedb_rl_requests
    '''
    result = await session.execute(select(ReferenceLetterRequest))
    rl_requests = result.scalars().all()
    return [ReferenceLetterRequest(name=rl_request.name, description=rl_request.description, id=rl_request.id) for rl_request in rl_requests]
    '''

@app.get("/rl_requests/{rl_request_id}")
def get_a_course(rl_request_id: int):
    rl_request = rl_request_id - 1
    return fakedb_rl_requests[rl_request]

#async
@app.post("/rl_requests")
def add_rl_request(rl_request: ReferenceLetterRequest):#ReferenceLetterRequestCreate, session: AsyncSession = Depends(get_session)):
    fakedb_rl_requests.append(rl_request.dict())
    return fakedb_rl_requests[-1]
    '''
    rl_request = ReferenceLetterRequest(name=rl_request.name, description=rl_request.description)
    session.add(rl_request)
    await session.commit()
    await session.refresh(rl_request)
    return rl_request
    '''

@app.delete("/rl_requests/{rl_request_id}")
def delete_rl_request(rl_request_id: int):
    fakedb_rl_requests.pop(rl_request_id - 1)
    return {"task": "deletion successful"}

# YT1
#async
@app.get("/students") #, response_model=List[Student])
def get_students():#session: AsyncSession = Depends(get_session)):
    return fakedb_students
    '''
    result = await session.execute(select(Student))
    students = result.scalars().all()
    return [Student(name=student.name, email=student.email, school_id=student.school_id, id=student.id) for student in students]
    '''

@app.get("/students/{student_id}")
def get_a_student(student_id: int):
    student = student_id - 1
    return fakedb_students[student]

#async
@app.post("/students")
def add_student(student: Student):#StudentCreate, session: AsyncSession = Depends(get_session)):
    fakedb_students.append(student.dict())
    return fakedb_students[-1]
    '''
    student = Student(name=student.name, email=student.email, school_id=student.school_id)
    session.add(student)
    await session.commit()
    await session.refresh(rl_request)
    return student
    '''

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    fakedb_students.pop(student_id - 1)
    return {"task": "deletion successful"}

# YT1
#async
@app.get("/teachers") #, response_model=List[Teacher])
def get_teachers():#session: AsyncSession = Depends(get_session)):
    return fakedb_teachers
    '''
    result = await session.execute(select(Teacher))
    teachers = result.scalars().all()
    return [Teacher(name=teacher.name, email=teacher.email, degree=teacher.degree, id=teacher.id) for teacher in teachers]
    '''

@app.get("/teachers/{teacher_id}")
def get_a_teacher(teacher_id: int):
    teacher = teacher_id - 1
    return fakedb_teachers[teacher]

#async
@app.post("/teachers")
def add_teacher(teacher: Teacher):#TeacherCreate, session: AsyncSession = Depends(get_session)):
    fakedb_teachers.append(teacher.dict())
    return fakedb_teachers[-1]
    '''
    teacher = Teacher(name=teacher.name, email=teacher.email, degree=teacher.degree)
    session.add(teacher)
    await session.commit()
    await session.refresh(teacher)
    return teacher
    '''

@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int):
    fakedb_teachers.pop(teacher_id - 1)
    return {"task": "deletion successful"}