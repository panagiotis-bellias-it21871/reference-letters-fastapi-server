from fastapi import Depends, FastAPI

'''
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ref_letters.db import get_session, init_db
from ref_letters.models import ReferenceLetterRequest, ReferenceLetterRequestCreate, Student, StudentCreate, Teacher, TeacherCreate
'''
from schemas import User #ReferenceLetterRequest
from utils import get_current_user
from db import database

# YT1
from schemas import fakedb, ReferenceLetterRequest

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await database.connect()
    # await init_db()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

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
    return fakedb
    '''
    result = await session.execute(select(ReferenceLetterRequest))
    rl_requests = result.scalars().all()
    return [ReferenceLetterRequest(name=rl_request.name, description=rl_request.description, id=rl_request.id) for rl_request in rl_requests]
    '''

@app.get("/rl_requests/{rl_request_id}")
def get_a_course(rl_request_id: int):
    rl_request = rl_request_id - 1
    return fakedb[rl_request]

#async
@app.post("/rl_requests")
def add_rl_request(rl_request: ReferenceLetterRequest):#ReferenceLetterRequestCreate, session: AsyncSession = Depends(get_session)):
    fakedb.append(rl_request.dict())
    return fakedb[-1]
    '''
    rl_request = ReferenceLetterRequest(name=rl_request.name, description=rl_request.description)
    session.add(rl_request)
    await session.commit()
    await session.refresh(rl_request)
    return rl_request
    '''

@app.delete("/rl_requests/{rl_request_id}")
def delete_rl_request(rl_request_id: int):
    fakedb.pop(rl_request_id - 1)
    return {"task": "deletion successful"}

@app.get("/students", response_model=List[Student])
async def get_students(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Student))
    students = result.scalars().all()
    return [Student(name=student.name, email=student.email, school_id=student.school_id, id=student.id) for student in students]

@app.post("/students")
async def add_student(student: StudentCreate, session: AsyncSession = Depends(get_session)):
    student = Student(name=student.name, email=student.email, school_id=student.school_id)
    session.add(student)
    await session.commit()
    await session.refresh(student)
    return student

@app.get("/teachers", response_model=List[Teacher])
async def get_teachers(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Teacher))
    teachers = result.scalars().all()
    return [Teacher(name=teacher.name, email=teacher.email, degree=teacher.degree, id=teacher.id) for teacher in teachers]

@app.post("/teachers")
async def add_teacher(teacher: TeacherCreate, session: AsyncSession = Depends(get_session)):
    teacher = Teacher(name=teacher.name, email=teacher.email, degree=teacher.degree)
    session.add(teacher)
    await session.commit()
    await session.refresh(teacher)
    return teacher