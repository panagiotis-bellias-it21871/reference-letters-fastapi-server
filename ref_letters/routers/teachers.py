from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from .. import schemas
from ..database import User, Teacher, async_session_maker as async_session
from ..users import current_active_user
from ..data_access_layer import TeacherDAL

router = APIRouter(prefix='/api/teachers')

@router.post("/")
async def create_teacher(teacher: schemas.TeacherCreate):
    async with async_session() as session:
        async with session.begin():
            teacher_dal = TeacherDAL(session)
            return await teacher_dal.create_teacher(teacher.description, teacher.user_username)

@router.get("/")
async def get_all_teachers(user: User = Depends(current_active_user)) -> List[Teacher]:
    if user.is_superuser or user.student:
        async with async_session() as session:
            async with session.begin():
                teacher_dal = TeacherDAL(session)
                return await teacher_dal.get_all_teachers()
    else:
        raise HTTPException(status_code=403, detail="Only students and admins can access these resources")

@router.get("/{teacher_id}")
async def get_a_teacher(teacher_id: int, user: User = Depends(current_active_user)) -> Teacher:
    if not user:
        raise HTTPException(status_code=403, detail="Only system users can access these resources")
    async with async_session() as session:
        async with session.begin():
            teacher_dal = TeacherDAL(session)
            return await teacher_dal.get_a_teacher(teacher_id)

@router.put("/{teacher_id}")
async def update_a_teacher(teacher_id: int, name: Optional[str] = None, description: Optional[str] = None, 
        user: User = Depends(current_active_user)):
    if user.is_superuser or user.teacher:
        async with async_session() as session:
            async with session.begin():
                teacher_dal = TeacherDAL(session)
                return await teacher_dal.update_teacher(teacher_id, name, description)
    else:
        raise HTTPException(status_code=403, detail="Only teachers and admins can access these resources")