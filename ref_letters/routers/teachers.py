from typing import List, Optional
from fastapi import APIRouter
from .. import schemas
from ..database import Teacher, async_session_maker as async_session
from ..data_access_layer import TeacherDAL

router = APIRouter(prefix='/api/teachers')

@router.post("/")
async def create_teacher(teacher: schemas.TeacherCreate):
    async with async_session() as session:
        async with session.begin():
            teacher_dal = TeacherDAL(session)
            return await teacher_dal.create_teacher(teacher.name, teacher.description)

@router.get("/")
async def get_all_teachers() -> List[Teacher]:
    async with async_session() as session:
        async with session.begin():
            teacher_dal = TeacherDAL(session)
            return await teacher_dal.get_all_teachers()

@router.get("/{teacher_id}")
async def get_a_teacher(teacher_id: int) -> Teacher:
    async with async_session() as session:
        async with session.begin():
            teacher_dal = TeacherDAL(session)
            return await teacher_dal.get_a_teacher(teacher_id)

@router.put("/{teacher_id}")
async def update_a_teacher(teacher_id: int, name: Optional[str] = None, description: Optional[str] = None):
    async with async_session() as session:
        async with session.begin():
            teacher_dal = TeacherDAL(session)
            return await teacher_dal.update_teacher(teacher_id, name, description)