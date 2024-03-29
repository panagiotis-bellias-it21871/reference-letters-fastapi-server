from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from .. import schemas
from ..users import current_active_user, User
from ..database import ReferenceLetterRequest, async_session_maker as async_session
from ..data_access_layer import ReferenceLetterRequestDAL
from . import send_email
from . import students

router = APIRouter(prefix='/api/rl_requests')

# get for a student
@router.get("/s/{student_id}")
async def get_students_rl_requests(student_id: int, user: User = Depends(current_active_user)) -> List[ReferenceLetterRequest]:
    if user.is_superuser or user.student:
        async with async_session() as session:
            async with session.begin():
                rl_request_dal = ReferenceLetterRequestDAL(session)
                return await rl_request_dal.get_students_rl_requests(student_id)
    else:
        raise HTTPException(status_code=403, detail="Only students and admins can access these resources")

# get pending for a teacher
@router.get("/t/pending/{teacher_id}")
async def get_pending_for_teacher(teacher_id: int, user: User = Depends(current_active_user)) -> List[ReferenceLetterRequest]:
    if user.is_superuser or user.teacher:
        async with async_session() as session:
            async with session.begin():
                rl_request_dal = ReferenceLetterRequestDAL(session)
                return await rl_request_dal.get_pending_for_teacher(teacher_id)
    else:
        raise HTTPException(status_code=403, detail="Only teachers and admins can access these resources")

'''
async def retrieveMailAddress(rl_request_id: int):
    email_address = ""
    # get rl_request and its student id
    rl_request = get_a_rl_request(rl_request_id)
    print("RL Request: ", rl_request)
    student_id = rl_request.student_id
    # get student by student id and its email
    email_address = students.get_a_student(student_id)
    print("Email address: ", email_address)

    return email_address
'''

# approve a pending
@router.put("/t/{rl_request_id}/approve")
async def approve_rl_request(rl_request_id: int, text: str, user: User = Depends(current_active_user)):
    if user.teacher:
        #email_address = await retrieveMailAddress(rl_request_id)
        async with async_session() as session:
            async with session.begin():
                rl_request_dal = ReferenceLetterRequestDAL(session)
                #print(email_address)
                email = {
                    "subject": "Approved Reference Letter Request",
                    # "email": [str(email_address)],
                    "email": ["belliaspan@gmail.com"],
                    "body": {
                        "title": "Approved Reference Letter Request",
                        "message": f"Your reference letter request with id: {rl_request_id} has been approved by the related teacher."
                    }
                }
                print(await send_email.send_email_async(email))
                return await rl_request_dal.approve_rl_request(rl_request_id, text)
    else:
        raise HTTPException(status_code=403, detail="Only teachers can perform these operations")

# decline a pending
@router.delete("/t/{rl_request_id}/decline")
async def decline_rl_request(rl_request_id: int, user: User = Depends(current_active_user)):
    if user.teacher:
        #email_address = retrieveMailAddress(rl_request_id)
        async with async_session() as session:
            async with session.begin():
                rl_request_dal = ReferenceLetterRequestDAL(session)
                email = {
                    "subject": "Declined Reference Letter Request",
                    "email": ["belliaspan@gmail.com"],
                    "body": {
                        "title": "Declined Reference Letter Request",
                        "message": f"Your reference letter request with id: {rl_request_id} has been declined by the related teacher."
                    }
                }
                print(await send_email.send_email_async(email))
                return await rl_request_dal.decline_rl_request(rl_request_id)
    else:
        raise HTTPException(status_code=403, detail="Only teachers can perform these operations")

@router.post("/")
async def create_rl_request(rl_request: schemas.ReferenceLetterRequestCreate, user: User = Depends(current_active_user)):
    if user.student:
        async with async_session() as session:
            async with session.begin():
                rl_request_dal = ReferenceLetterRequestDAL(session)
                return await rl_request_dal.create_rl_request(rl_request.teacher_id, rl_request.student_id, 
                    rl_request.carrier_name, rl_request.carrier_email, rl_request.status, rl_request.text)
    else:
        raise HTTPException(status_code=403, detail="Only students can perform these operations")

@router.get("/")
async def get_all_rl_requests(user: User = Depends(current_active_user)) -> List[ReferenceLetterRequest, ]:
    #if user.is_superuser:
        async with async_session() as session:
            async with session.begin():
                rl_request_dal = ReferenceLetterRequestDAL(session)
                return await rl_request_dal.get_all_rl_requests()
    #else:
    #    raise HTTPException(status_code=403, detail="Only admins can access these resources")
# stopped here with endpoint protection
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