from typing import Optional
from fastapi import FastAPI

from minio import Minio
from minio.error import S3Error
import os

app = FastAPI()

# Create a client with the MinIO server playground, its access key
# and secret key.
client = Minio(
    str(os.getenv("MIN_IO_SERVER", default="localhost")),
    access_key=os.getenv("MIN_IO_ACCESS_KEY"),
    secret_key=os.getenv("MIN_IO_SECRET_KEY")
)
# Make 'asiatrip' bucket if not exist.
bucket = os.getenv("MIN_IO_BUCKET_NAME")
found = client.bucket_exists(bucket)
if not found:
    client.make_bucket(bucket)
else:
    print(f"Bucket {bucket} already exists")

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

@app.get("/test-minio")
async def test_minio():
    try:
        # Upload '/home/user/Photos/asiaphotos.zip' as object name
        # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
        client.fput_object(
            bucket, "test-09-03-2022.zip", "../README.md",
        )
        print(
            f"'README.md' is successfully uploaded as "
            "object 'test-09-03-2022.zip' to bucket {bucket}."
        )
        message = "Success!"
    except S3Error as exc:
        message = f"error occurred. {exc}"
        print(message)
    return {"message": message}