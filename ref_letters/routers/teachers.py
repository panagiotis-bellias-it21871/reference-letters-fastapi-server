from fastapi import APIRouter
from ..db import database, teacher_db
from ..schemas import Teacher

router = APIRouter()

@router.get("/teachers")
async def get_teachers():
    query = teacher_db.select()
    all_get = await database.fetch_all(query)
    return all_get

@router.get("/teachers/{teacher_id}")
async def get_a_teacher(teacher_id: int):
    query = teacher_db.select().where(teacher_db.c.id == teacher_id)
    user = await database.fetch_one(query)
    return {**user}

@router.post("/teachers")
async def add_teacher(teacher: Teacher):
    query = teacher_db.insert().values(
        name=teacher.name,
        email=teacher.email,
        description=teacher.description,
    )
    record_id = await database.execute(query)
    query = teacher_db.select().where(teacher_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@router.put("/teachers/{teacher_id}")
async def update_teacher(teacher_id: int, teacher: Teacher):
    query = teacher_db.update().where(teacher_db.c.id == teacher_id).values(
        name=teacher.name,
        email=teacher.email,
        description=teacher.description,
    )
    record_id = await database.execute(query)
    query = teacher_db.select().where(teacher_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@router.delete("/teachers/{teacher_id}")
async def delete_teacher(teacher_id: int):
    query = teacher_db.delete().where(teacher_db.c.id == teacher_id)
    return await database.execute(query)