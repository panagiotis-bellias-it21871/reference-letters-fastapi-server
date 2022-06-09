from fastapi import APIRouter
from ..db import database, student_db
from ..schemas import Student

router = APIRouter()

@router.get("/students")
async def get_students():
    query = student_db.select()
    all_get = await database.fetch_all(query)
    return all_get

@router.get("/students/{student_id}")
async def get_a_student(student_id: int):
    query = student_db.select().where(student_db.c.id == student_id)
    user = await database.fetch_one(query)
    return {**user}

@router.post("/students")
async def add_student(student: Student):
    query = student_db.insert().values(
        name=student.name,
        school_id=student.school_id,
        email=student.email
    )
    record_id = await database.execute(query)
    query = student_db.select().where(student_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@router.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
    query = student_db.update().where(student_db.c.id == student_id).values(
        name=student.name,
        school_id=student.school_id,
        email=student.email
    )
    record_id = await database.execute(query)
    query = student_db.select().where(student_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@router.delete("/students/{student_id}")
async def delete_student(student_id: int):
    query = student_db.delete().where(student_db.c.id == student_id)
    return await database.execute(query)