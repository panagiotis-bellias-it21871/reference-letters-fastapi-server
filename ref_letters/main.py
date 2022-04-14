import email
from fastapi import Depends, FastAPI
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from ref_letters.database import get_session, init_db
from ref_letters.models import ReferenceLetterRequest, ReferenceLetterRequestCreate, Student, StudentCreate, Teacher, TeacherCreate

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}

@app.get("/rl_requests", response_model=list[ReferenceLetterRequest])
async def get_rl_requests(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ReferenceLetterRequest))
    rl_requests = result.scalars().all()
    return [ReferenceLetterRequest(name=rl_request.name, description=rl_request.description, id=rl_request.id) for rl_request in rl_requests]

@app.post("/rl_requests")
async def add_rl_request(rl_request: ReferenceLetterRequestCreate, session: AsyncSession = Depends(get_session)):
    rl_request = ReferenceLetterRequest(name=rl_request.name, description=rl_request.description)
    session.add(rl_request)
    await session.commit()
    await session.refresh(rl_request)
    return rl_request

@app.get("/students", response_model=list[Student])
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

@app.get("/teachers", response_model=list[Teacher])
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