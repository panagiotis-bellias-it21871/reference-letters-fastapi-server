from typing import AsyncGenerator, Optional

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy import AsyncSession, SQLAlchemyUserDatabase
from pydantic import BaseModel
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from .db import engine

Base: DeclarativeMeta = declarative_base()

class ReferenceLetterRequest(BaseModel):
    id: int
    teacher_id: int
    student_id: int
    carrier_name: str
    carrier_email: str
    status: str
    text: str

class Student(BaseModel):
    id: int
    name: str
    email: str
    school: str
    school_id: str
    grades_url: str

class Teacher(BaseModel):
    id: int
    name: str
    email: str
    description: str

class User(SQLAlchemyBaseUserTableUUID, Base):
    username: str
    email: str
    full_name: str
    student: bool
    teacher: bool
    admin: bool
    disabled: Optional[bool] = None

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

class UserInDB(User):
    hashed_password: str
