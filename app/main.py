from typing import Optional
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to reference letters web system @HUA-DIT!"}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/reference_letter_requests/{reference_letter_request_id}")
async def read_reference_letter_request(reference_letter_request_id: int, q: Optional[str] = None):
    return {"reference_letter_request_id": reference_letter_request_id, "q": q}

@app.get("/grading_files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}