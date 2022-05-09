import databases
import sqlalchemy
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

DATABASE_URL = os.getenv("DATABASE_URL", default="")
metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)
reference_letter_request_db = sqlalchemy.Table(
    "reference_letter_request",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(500)),
    sqlalchemy.Column("is_approved", sqlalchemy.Boolean),
    sqlalchemy.Column("is_declined", sqlalchemy.Boolean),
    sqlalchemy.Column("is_pending", sqlalchemy.Boolean),
)

student_db = sqlalchemy.Table(
    "student",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(500)),
    sqlalchemy.Column("school_id", sqlalchemy.String(125)),
    sqlalchemy.Column("email", sqlalchemy.String(750)),
)

teacher_db = sqlalchemy.Table(
    "teacher",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(500)),
    sqlalchemy.Column("email", sqlalchemy.String(750)),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)

"""
import os

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
"""

'''
async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
'''
#import databases


# SQLAlchemy specific code, as with any other app
#DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

#database = databases.Database(DATABASE_URL)

'''
async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
'''