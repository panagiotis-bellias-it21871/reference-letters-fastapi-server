from typing import List, Optional
from fastapi import APIRouter
from .. import schemas
from ..database import ReferenceLetterRequest, async_session_maker as async_session
from ..data_access_layer import ReferenceLetterRequestDAL

router = APIRouter(prefix='/api/rl_requests')

# get for a student
@router.get("/{student_id}")
async def get_students_rl_requests(student_id: int) -> List[ReferenceLetterRequest]:
    async with async_session() as session:
        async with session.begin():
            rl_request_dal = ReferenceLetterRequestDAL(session)
            return await rl_request_dal.get_students_rl_requests(student_id)

# get pending for a teacher
@router.get("/pending/{teacher_id}")
async def get_pending_for_teacher(teacher_id: int) -> List[ReferenceLetterRequest]:
    async with async_session() as session:
        async with session.begin():
            rl_request_dal = ReferenceLetterRequestDAL(session)
            return await rl_request_dal.get_pending_for_teacher(teacher_id)

# approve a pending
@router.put("{rl_request_id}/approve")
async def approve_rl_request(rl_request_id: int, text: str):
    async with async_session() as session:
        async with session.begin():
            rl_request_dal = ReferenceLetterRequestDAL(session)
            # send mail here
            return await rl_request_dal.approve_rl_request(rl_request_id, text)

# decline a pending
@router.delete("{rl_request_id}/decline")
async def decline_rl_request(rl_request_id: int):
    async with async_session() as session:
        async with session.begin():
            rl_request_dal = ReferenceLetterRequestDAL(session)
            # send mail here
            return await rl_request_dal.decline_rl_request(rl_request_id)

@router.post("/")
async def create_rl_request(rl_request: schemas.ReferenceLetterRequestCreate):
    async with async_session() as session:
        async with session.begin():
            rl_request_dal = ReferenceLetterRequestDAL(session)
            return await rl_request_dal.create_rl_request(rl_request.teacher_id, rl_request.student_id, 
                rl_request.carrier_name, rl_request.carrier_email, rl_request.status, rl_request.text)

@router.get("/")
async def get_all_rl_requests() -> List[ReferenceLetterRequest]:
    async with async_session() as session:
        async with session.begin():
            rl_request_dal = ReferenceLetterRequestDAL(session)
            return await rl_request_dal.get_all_rl_requests()

@router.get("/{rl_request_id}")
async def get_a_rl_request(rl_request_id: int) -> ReferenceLetterRequest:
    async with async_session() as session:
        async with session.begin():
            rl_request_dal = ReferenceLetterRequestDAL(session)
            return await rl_request_dal.get_a_rl_request(rl_request_id)

@router.put("/{rl_request_id}")
async def update_rl_request(rl_request_id: int, teacher_id: Optional[int] = None, student_id: Optional[int] = None, 
            carrier_name: Optional[str] = None, carrier_email: Optional[str] = None, status: Optional[str] = None, text: Optional[str] = None):
    async with async_session() as session:
        async with session.begin():
            rl_request_dal = ReferenceLetterRequestDAL(session)
            return await rl_request_dal.update_rl_request(rl_request_id, teacher_id, student_id, carrier_name, 
                carrier_email, status, text)