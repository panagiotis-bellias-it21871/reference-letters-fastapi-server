import os
import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, schemas
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users.db import SQLAlchemyUserDatabase

from .database import User, get_user_db
from .routers import send_email as mail

SECRET = os.getenv("SECRET", default="SECRET")
HOST = os.getenv("ORIGIN", default="http://localhost:8080")

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
        email = {
            "subject": "Email Verification",
            "email": [user.email],
            "body": {
                "host": HOST,
                "token": token
            }
        }
        print(await mail.send_email_async(email))

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)

class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
    full_name: str
    student: bool
    teacher: bool

class UserCreate(schemas.BaseUserCreate):
    username: str
    full_name: str
    student: bool
    teacher: bool

class UserUpdate(schemas.BaseUserUpdate):
    username: str
    full_name: str
    student: bool
    teacher: bool
