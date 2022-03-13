import json
import logging
from typing import Optional, Dict

import jwt
import requests
from fastapi import FastAPI, Path, Query
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.responses import RedirectResponse

import minio_functions
import keycloak_functions
from models import ReferenceLetterRequest

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to reference letters web system @HUA-DIT!"}

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
    return minio_functions.test()

@app.get("/test_keycloak/login")
async def test_keycloak_login() -> RedirectResponse:
    return RedirectResponse(keycloak_functions.AUTH_URL)

@app.get("/test_keycloak/auth")
async def test_keycloak_auth() -> RedirectResponse:
    payload = (
        f"grant_type=authorization_code&code=code"
        f"&redirect_uri={keycloak_functions.APP_BASE_URL}&client_id={keycloak_functions.CLIENT_ID}"
    )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_response = requests.request(
        "POST", keycloak_functions.TOKEN_URL, data=payload, headers=headers
    )

    token_body = json.loads(token_response.content)
    access_token = token_body["access_token"]

    response = RedirectResponse(url="/")
    response.set_cookie("Authorization", value=f"Bearer {access_token}")
    return response

@app.get("/")
async def root(request: Request,) -> Dict:
    authorization: str = request.cookies.get("Authorization")
    scheme, credentials = get_authorization_scheme_param(authorization)

    decoded = jwt.decode(
        credentials, verify=False
    )  # TODO input keycloak public key as key, disable option to verify aud
    logger.debug(decoded)

    return {"message": "You're logged in!"}