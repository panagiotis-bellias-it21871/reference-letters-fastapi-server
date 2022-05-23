import os
from dotenv import load_dotenv

from fastapi import Depends, FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi_keycloak import FastAPIKeycloak, OIDCUser

from .db import database, reference_letter_request_db, student_db, teacher_db

from .schemas import ReferenceLetterRequest, Student, Teacher, User

load_dotenv(verbose=True)

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
idp = FastAPIKeycloak(
    server_url=os.getenv("KC_SERVER_URL", default=""),
    client_id=os.getenv("KC_CLIENT_URL", default="some-client"),
    client_secret=os.getenv("KC_CLIENT_SECRET", default="some-client-secret"),
    admin_client_secret=os.getenv("KC_ADMIN_CLIENT_SECRET", default="admin-cli-secret"),
    realm=os.getenv("KC_REALM", default="some-realm-name"),
    callback_uri=os.getenv("KC_CALLBACK_URI", default="http://localhost:8081/callback")
)
idp.add_swagger_config(app)
"""

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return {"greetings": "Welcome to FastAPI Python"}

"""
@app.get("/admin")
def admin(user: OIDCUser = Depends(idp.get_current_user(required_roles=["admin"]))):
    return f'Hi premium user{user}'

@app.get("/user/roles")
def user_roles(user: OIDCUser = Depends(idp.get_current_user)):
    return f'{user.roles}'
"""

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}

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