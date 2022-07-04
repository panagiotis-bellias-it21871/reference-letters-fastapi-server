import os
from dotenv import load_dotenv
from fastapi import FastAPI, Form #, Depends
from fastapi.middleware.cors import CORSMiddleware

from .routers import rl_requests, students, teachers #, keycloak_user_handling
from .db import database

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

app.include_router(rl_requests.router)
app.include_router(students.router)
app.include_router(teachers.router)
#app.include_router(keycloak_user_handling.router)

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
