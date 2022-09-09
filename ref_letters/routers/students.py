from typing import List, Optional
from fastapi import APIRouter
from .. import schemas
from ..database import Student, async_session_maker as async_session
from ..users import current_active_user
from ..data_access_layer import StudentDAL

router = APIRouter(prefix='/api/students')

@router.post("/")
async def create_student(student: schemas.StudentCreate):
    async with async_session() as session:
        async with session.begin():
            student_dal = StudentDAL(session)
            return await student_dal.create_student(student.name, student.school, student.school_id, student.grades_url)

@router.get("/")
async def get_all_students(user: User = Depends(current_active_user)) -> List[Student]:
    if user.is_superuser:
        async with async_session() as session:
            async with session.begin():
                student_dal = StudentDAL(session)
                return await student_dal.get_all_students()
    else:
        raise HTTPException(status_code=403, detail="Only admins can access these resources")

@router.get("/{student_id}")
async def get_a_student(student_id: int, user: User = Depends(current_active_user)) -> Student:
    if not user:
        raise HTTPException(status_code=403, detail="Only system users can access these resources")
    async with async_session() as session:
        async with session.begin():
            student_dal = StudentDAL(session)
            return await student_dal.get_a_student(student_id)

@router.put("/{student_id}")
async def update_a_student(student_id: int, name: Optional[str] = None, school: Optional[str] = None, school_id: Optional[str] = None, 
        grades_url: Optional[str] = None, user: User = Depends(current_active_user)):
    if user.is_superuser or user.student:
        async with async_session() as session:
            async with session.begin():
                student_dal = StudentDAL(session)
                return await student_dal.update_student(student_id, name, school, school_id, grades_url)
    else:
        raise HTTPException(status_code=403, detail="Only students and admins can access these resources")