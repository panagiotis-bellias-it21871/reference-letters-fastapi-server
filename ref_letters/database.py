import os
from typing import AsyncGenerator

import databases
import sqlalchemy
from dotenv import load_dotenv
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy import AsyncSession, SQLAlchemyUserDatabase
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker, relationship

load_dotenv(verbose=True)

DATABASE_URL = os.getenv("DATABASE_URL", default="")             # Declare database url (e.g. sqlite or postgreSQL)
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base: DeclarativeMeta = declarative_base()

class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    description = Column(String)

    reference_letter_requests = relationship("ReferenceLetterRequest", back_populates="to_teacher")

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    school = Column(String)
    school_id = Column(String)
    grades_url = Column(String)

    reference_letter_requests = relationship("ReferenceLetterRequest", back_populates="from_student")

class ReferenceLetterRequest(Base):
    __tablename__ = "reference_letter_request"
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    student_id = Column(Integer, ForeignKey("student.id"))
    carrier_name = Column(String)
    carrier_email = Column(String)
    status = Column(String)
    text = Column(String)

    to_teacher = relationship("Teacher", back_populates="reference_letter_requests")
    from_student = relationship("Student", back_populates="reference_letter_requests")

class User(SQLAlchemyBaseUserTableUUID, Base):
    username = Column(String)
    email = Column(String)
    full_name = Column(String)
    student = Column(Boolean)
    teacher = Column(Boolean)
    admin = Column(Boolean)
    disabled = Column(Boolean)

async def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
    #async with engine.begin() as conn:
    #    await conn.run_sync(Base.metadata.create_all)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

class UserInDB(User):
    hashed_password: str
