from fastapi import APIRouter
from ref_letters.db import database, reference_letter_request_db
from ref_letters.schemas import ReferenceLetterRequest

router = APIRouter()

@router.get("/rl_requests")
async def get_rl_requests():
    query = reference_letter_request_db.select()
    all_get = await database.fetch_all(query)
    return all_get

@router.get("/rl_requests/{rl_request_id}")
async def get_a_rl_request(rl_request_id: int):
    query = reference_letter_request_db.select().where(reference_letter_request_db.c.id == rl_request_id)
    user = await database.fetch_one(query)
    return {**user}

@router.post("/rl_requests")
async def add_rl_request(rl_request: ReferenceLetterRequest):
    query = reference_letter_request_db.insert().values(
        name=rl_request.name,
        is_approved=rl_request.is_approved,
        is_declined=rl_request.is_declined,
        is_pending=rl_request.is_pending
    )
    record_id = await database.execute(query)
    query = reference_letter_request_db.select().where(reference_letter_request_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@router.put("/rl_requests/{rl_request_id}")
async def update_rl_request(rl_request_id: int, rl_request: ReferenceLetterRequest):
    query = reference_letter_request_db.update().where(reference_letter_request_db.c.id == rl_request_id).values(
        name=rl_request.name,
        is_approved=rl_request.is_approved,
        is_declined=rl_request.is_declined,
        is_pending=rl_request.is_pending
    )
    record_id = await database.execute(query)
    query = reference_letter_request_db.select().where(reference_letter_request_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@router.delete("/rl_requests/{rl_request_id}")
async def delete_rl_request(rl_request_id: int):
    query = reference_letter_request_db.delete().where(reference_letter_request_db.c.id == rl_request_id)
    return await database.execute(query)