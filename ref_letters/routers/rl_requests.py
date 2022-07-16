from fastapi import APIRouter
from ..db import database, reference_letter_request_db
from ..schemas import ReferenceLetterRequest

router = APIRouter(prefix='/api/rl_requests')

@router.get("/")
async def get_rl_requests():
    query = reference_letter_request_db.select()
    all_get = await database.fetch_all(query)
    return all_get

@router.get("/{rl_request_id}")
async def get_a_rl_request(rl_request_id: int):
    query = reference_letter_request_db.select().where(reference_letter_request_db.c.id == rl_request_id)
    user = await database.fetch_one(query)
    return {**user}

@router.post("/")
async def add_rl_request(rl_request: ReferenceLetterRequest):
    query = reference_letter_request_db.insert().values(
        teacher_id=rl_request.teacher_id,
        student_id=rl_request.student_id,
        carrier_name=rl_request.carrier_name,
        carrier_email=rl_request.carrier_email,
        status=rl_request.status,
        text=rl_request.text
    )
    record_id = await database.execute(query)
    query = reference_letter_request_db.select().where(reference_letter_request_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@router.put("/{rl_request_id}")
async def update_rl_request(rl_request_id: int, rl_request: ReferenceLetterRequest):
    query = reference_letter_request_db.update().where(reference_letter_request_db.c.id == rl_request_id).values(
        teacher_id=rl_request.teacher_id,
        student_id=rl_request.student_id,
        carrier_name=rl_request.carrier_name,
        carrier_email=rl_request.carrier_email,
        status=rl_request.status,
        text=rl_request.text
    )
    record_id = await database.execute(query)
    query = reference_letter_request_db.select().where(reference_letter_request_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@router.delete("/{rl_request_id}")
async def delete_rl_request(rl_request_id: int):
    query = reference_letter_request_db.delete().where(reference_letter_request_db.c.id == rl_request_id)
    return await database.execute(query)
