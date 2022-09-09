from typing import AsyncGenerator

import databases
import sqlalchemy
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy import AsyncSession, SQLAlchemyUserDatabase
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

DATABASE_URL = os.getenv("DATABASE_URL", default="sqlite+aiosqlite:///./test.db")   # Declare database url
database = databases.Database(DATABASE_URL)
Base: DeclarativeMeta = declarative_base()
engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    user_username = Column(String, ForeignKey("user.username"))
    user = relationship("User")

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    school = Column(String)
    school_id = Column(String)
    grades_url = Column(String)
    user_username = Column(String, ForeignKey("user.username"))
    user = relationship("User")

class ReferenceLetterRequest(Base):
    __tablename__ = "reference_letter_request"
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    student_id = Column(Integer, ForeignKey("student.id"))
    carrier_name = Column(String)
    carrier_email = Column(String)
    status = Column(String)
    text = Column(String)

class User(SQLAlchemyBaseUserTableUUID, Base):
    username = Column(String, unique=True)
    email = Column(String)
    full_name = Column(String)
    student = Column(Boolean)
    teacher = Column(Boolean)
    admin = Column(Boolean)
    disabled = Column(Boolean)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
