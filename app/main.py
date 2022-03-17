from typing import Optional
from fastapi import FastAPI, Path, Query
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import ReferenceLetterRequest as SchemaReferenceLetterRequest
from schema import Student as SchemaStudent
from schema import Teacher as SchemaTeacher
from schema import ReferenceLetterRequest, Student, Teacher

from models import ReferenceLetterRequest as ModelReferenceLetterRequest
from models import Student as ModelStudent
from models import Teacher as ModelTeacher

import env_store as env
import minio_api, keycloak_api
from models import ReferenceLetterRequest, Student, Teacher

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=env.db_url)

"""
Home Page API
"""
@app.get("/")
async def root():
    return {"message": "Welcome to reference letters web system @HUA-DIT!"}

"""
Reference Letter Requests API
"""
@app.post('/reference_letter_request/', response_model=SchemaReferenceLetterRequest)
async def post_reference_letter_request(reference_letter_request: SchemaReferenceLetterRequest):
    db_reference_letter_request = 
        ModelReferenceLetterRequest(name=reference_letter_request.name, description=reference_letter_request.description)
    db.session.add(db_reference_letter_request)
    db.session.commit()
    return db_reference_letter_request

@app.get('/reference_letter_requests/')
async def get_reference_letter_requests():
    reference_letter_requests = db.session.query(ModelReferenceLetterRequest).all()
    return reference_letter_requests

@app.get("/reference_letter_requests/{reference_letter_request_id}")
async def get_reference_letter_request(
    reference_letter_request_id: int = Path(..., title="The ID of the reference letter request to get")
    ):
    reference_letter_request = db.session.query(ModelReferenceLetterRequest).get(reference_letter_request_id)
    return reference_letter_request

@app.put("/reference_letter_requests/{reference_letter_request_id}")
async def put_reference_letter_request(reference_letter_request_id: int, reference_letter_request: SchemaReferenceLetterRequest):
    db.session.query(ModelReferenceLetterRequest).filter(ModelReferenceLetterRequest.id == reference_letter_request_id).
    update(reference_letter_request, synchronize_session = False)
    return db.session.commit()

"""
Students API
"""
@app.post('/student/', response_model=SchemaStudent)
async def post_student(student: SchemaStudent):
    db_student = 
        ModelStudent(name=student.name, email=student.email, school_id=student.school_id)
    db.session.add(db_student)
    db.session.commit()
    return db_student

@app.get('/students/')
async def get_students():
    students = db.session.query(ModelStudent).all()
    return students

@app.get("/students/{student_id}")
async def get_student(
    student_id: int = Path(..., title="The ID of the student to get")
    ):
    student = db.session.query(ModelStudent).get(student_id)
    return student

@app.put("/students/{student_id}")
async def put_student(student_id: int, student: SchemaStudent):
    db.session.query(ModelStudent).filter(ModelStudent.id == student_id).
    update(student, synchronize_session = False)
    return db.session.commit()

"""
Teachers API
"""
@app.post('/teacher/', response_model=SchemaTeacher)
async def post_teacher(teacher: SchemaTeacher):
    db_teacher = 
        ModelTeacher(name=teacher.name, email=teacher.email, degree=teacher.school_id)
    db.session.add(db_teacher)
    db.session.commit()
    return db_teacher

@app.get('/teachers/')
async def get_teachers():
    teachers = db.session.query(ModelTeacher).all()
    return teachers

@app.get("/teachers/{teacher_id}")
async def get_teacher(
    teacher_id: int = Path(..., title="The ID of the teacher to get")
    ):
    teacher = db.session.query(ModelTeacher).get(teacher_id)
    return teacher

@app.put("/teachers/{teacher_id}")
async def put_teacher(teacher_id: int, teacher: SchemaTeacher):
    db.session.query(ModelTeacher).filter(ModelTeacher.id == teacher_id).
    update(teacher, synchronize_session = False)
    return db.session.commit()

"""
Minio API
"""
@app.get("/grading_files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.get("/test_minio")
async def test_minio():
    return minio_api.test()

"""
KeyCloak API
"""
@app.get("/user")  # Requires logged in
def current_users():
    return keycloak_api.current_users()

@app.get("/admin")
def company_admin():
    return keycloak_api.company_admin()

@app.get("/login")
def login_redirect():
    return keycloak_api.login_redirect()

@app.get("/callback")
def callback(session_state: str, code: str):
    return keycloak_api.callback(session_state, code)

@app.get("/user/roles")
def user_roles():
    return keycloak_api.user_roles()

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str = Path(..., title="The ID of the user to get")):
    return {"user_id": user_id}