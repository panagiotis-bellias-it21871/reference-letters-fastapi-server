#import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

from .database import User, create_db_and_tables, database
from .routers import (rl_requests, students,  # , keycloak_user_handling
                      teachers)
from .users import (UserCreate, UserRead, UserUpdate, auth_backend,
                           current_active_user, fastapi_users)

load_dotenv(verbose=True)

origins = ["*"]
#origins = os.getenv("ORIGINS", default="http://127.0.0.1:8080/")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rl_requests.router,tags=["rl_requests"])
app.include_router(students.router,tags=["students"])
app.include_router(teachers.router,tags=["teachers"])
#app.include_router(keycloak_user_handling.router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"] 
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True),
    prefix="/users",
    tags=["users"]
)

@app.on_event("startup")
async def connect():
    await create_db_and_tables()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return {"greetings": "Welcome to FastAPI Python"}

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

@app.get("/ping")
async def ping():
    return {"ping": "pong!"}

@app.post("/language/")
async def language(name: str = Form(...), type: str = Form(...)):
    return {"name": name, "type": type}

"""
@app.get("/admin")
def admin(user: OIDCUser = Depends(idp.get_current_user(required_roles=["admin"]))):
    return f'Hi premium user{user}'

@app.get("/user/roles")
def user_roles(user: OIDCUser = Depends(idp.get_current_user)):
    return f'{user.roles}'
"""
