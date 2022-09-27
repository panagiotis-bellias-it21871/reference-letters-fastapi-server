'''main.py'''
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from .database import create_db_and_tables, database
from .routers import (home, rl_requests, students,  teachers)
from .users import (UserCreate, UserRead, UserUpdate, auth_backend, fastapi_users)

load_dotenv(verbose=True)

origin = os.getenv("ORIGIN", default=["http://localhost:8080/"])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    #allow_origins=origin,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(home.router,tags=["/"])
app.include_router(rl_requests.router,tags=["rl_requests"])
app.include_router(students.router,tags=["students"])
app.include_router(teachers.router,tags=["teachers"])

app.include_router(
    #fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True),
    fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=False),
    prefix="/users",
    tags=["users"]
)

app.include_router(
    #fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    fastapi_users.get_auth_router(auth_backend, requires_verification=False),
    prefix="/auth/jwt",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

@app.get("/")
async def root():
    response = RedirectResponse("/api/")
    return response

@app.on_event("startup")
async def connect():
    await create_db_and_tables()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
