from minio import Minio
from minio.error import S3Error

import os

bucket = os.getenv("MIN_IO_BUCKET_NAME")
access_key=os.getenv("MIN_IO_ACCESS_KEY")
secret_key=os.getenv("MIN_IO_SECRET_KEY")

def init():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        str(os.getenv("MIN_IO_SERVER", default="localhost")),
        access_key=access_key,
        secret_key=secret_key,
    )
    # Make 'asiatrip' bucket if not exist.
    found = client.bucket_exists(bucket)
    if not found:
        client.make_bucket(bucket)
    else:
        print(f"Bucket {bucket} already exists")
        client = found
    return client

def test():
    client = init()
    try:
        # Upload '/home/user/Photos/asiaphotos.zip' as object name
        # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
        client.fput_object(
            bucket, "test-09-03-2022.zip", "../README.md",
        )
        print(f"'README.md' is successfully uploaded as object 'test-09-03-2022.zip' to bucket {bucket}.")
        message = "Success!"
    except S3Error as exc:
        message = f"error occurred. {exc}"
        print(message)
    return {"message": message}