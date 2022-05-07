from fastapi import Depends, FastAPI, Form

from .utils import get_current_user
from .db import database, reference_letter_request_db, student_db, teacher_db

from .schemas import ReferenceLetterRequest, Student, Teacher, User

app = FastAPI()

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return {"greetings": "Welcome to FastAPI Python"}

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# YT2
@app.post("/language/")
async def language(name: str = Form(...), type: str = Form(...)):
    return {"name": name, "type": type}

@app.get("/rl_requests")
async def get_rl_requests():
    query = reference_letter_request_db.select()
    all_get = await database.fetch_all(query)
    return all_get

@app.get("/rl_requests/{rl_request_id}")
async def get_a_rl_request(rl_request_id: int):
    query = reference_letter_request_db.select().where(reference_letter_request_db.c.id == rl_request_id)
    user = await database.fetch_one(query)
    return {**user}

@app.post("/rl_requests")
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

@app.put("/rl_requests/{rl_request_id}")
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

@app.delete("/rl_requests/{rl_request_id}")
async def delete_rl_request(rl_request_id: int):
    query = reference_letter_request_db.delete().where(reference_letter_request_db.c.id == rl_request_id)
    return await database.execute(query)

@app.get("/students")
async def get_students():
    query = student_db.select()
    all_get = await database.fetch_all(query)
    return all_get

@app.get("/students/{student_id}")
async def get_a_student(student_id: int):
    query = student_db.select().where(student_db.c.id == student_id)
    user = await database.fetch_one(query)
    return {**user}

@app.post("/students")
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

@app.put("/students/{student_id}")
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

@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    query = student_db.delete().where(student_db.c.id == student_id)
    return await database.execute(query)

@app.get("/teachers")
async def get_teachers():
    query = teacher_db.select()
    all_get = await database.fetch_all(query)
    return all_get

@app.get("/teachers/{teacher_id}")
async def get_a_teacher(teacher_id: int):
    query = teacher_db.select().where(teacher_db.c.id == teacher_id)
    user = await database.fetch_one(query)
    return {**user}

@app.post("/teachers")
async def add_teacher(teacher: Teacher):
    query = teacher_db.insert().values(
        name=teacher.name,
        email=teacher.email
    )
    record_id = await database.execute(query)
    query = teacher_db.select().where(teacher_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@app.put("/teachers/{teacher_id}")
async def update_teacher(teacher_id: int, teacher: Teacher):
    query = teacher_db.update().where(teacher_db.c.id == teacher_id).values(
        name=teacher.name,
        email=teacher.email
    )
    record_id = await database.execute(query)
    query = teacher_db.select().where(teacher_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@app.delete("/teachers/{teacher_id}")
async def delete_teacher(teacher_id: int):
    query = teacher_db.delete().where(teacher_db.c.id == teacher_id)
    return await database.execute(query)