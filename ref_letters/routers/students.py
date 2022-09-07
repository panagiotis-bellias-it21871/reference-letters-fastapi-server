from typing import List, Optional
from fastapi import APIRouter
from .. import schemas
from ..database import Student, async_session_maker as async_session
from ..data_access_layer import StudentDAL

router = APIRouter(prefix='/api/students')

@router.post("/")
async def create_student(student: schemas.StudentCreate):
    async with async_session() as session:
        async with session.begin():
            student_dal = StudentDAL(session)
            return await student_dal.create_student(student.name, student.school, student.school_id, student.grades_url)

@router.get("/")
async def get_all_students() -> List[Student]:
    async with async_session() as session:
        async with session.begin():
            student_dal = StudentDAL(session)
            return await student_dal.get_all_students()

@router.get("/{student_id}")
async def get_a_student(student_id: int) -> Student:
    async with async_session() as session:
        async with session.begin():
            student_dal = StudentDAL(session)
            return await student_dal.get_a_student(student_id)

@router.put("/{student_id}")
async def update_a_student(student_id: int, name: Optional[str] = None, school: Optional[str] = None, school_id: Optional[str] = None, grades_url: Optional[str] = None):
    async with async_session() as session:
        async with session.begin():
            student_dal = StudentDAL(session)
            return await student_dal.update_student(name, school, school_id, grades_url):