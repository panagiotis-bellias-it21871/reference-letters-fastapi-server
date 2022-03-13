from typing import Optional
from fastapi import FastAPI, Path, Query

import minio_handler, keycloak_handler
from models import ReferenceLetterRequest

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to reference letters web system @HUA-DIT!"}

@app.get("/user")  # Requires logged in
def current_users():
    return keycloak_handler.current_users()

@app.get("/admin")
def company_admin():
    return keycloak_handler.company_admin()

@app.get("/login")
def login_redirect():
    return keycloak_handler.login_redirect()

@app.get("/callback")
def callback(session_state: str, code: str):
    return keycloak_handler.callback(session_state, code)

@app.get("/user/roles")
def user_roles():
    return keycloak_handler.user_roles()

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str = Path(..., title="The ID of the user to get")):
    return {"user_id": user_id}

@app.get("/reference_letter_requests/{reference_letter_request_id}")
async def read_reference_letter_request(
    reference_letter_request_id: int = Path(..., title="The ID of the reference letter request to get"),
    q: Optional[str] = Query(None, alias="reference-letter-request-query"),
    ):
    return {"reference_letter_request_id": reference_letter_request_id, "q": q}

@app.post("/reference_letter_requests/")
async def create_reference_letter_request(referenceLetterRequest: ReferenceLetterRequest):
    referenceLetterRequest_dict = referenceLetterRequest.dict()
    return referenceLetterRequest_dict

@app.put("/reference_letter_requests/{reference_letter_request_id}")
async def update_reference_letter_request(reference_letter_request_id: int, referenceLetterRequest: ReferenceLetterRequest):
    return {"reference_letter_request_id": reference_letter_request_id, **referenceLetterRequest.dict()}

@app.get("/grading_files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.get("/test_minio")
async def test_minio():
    return minio_handler.test()