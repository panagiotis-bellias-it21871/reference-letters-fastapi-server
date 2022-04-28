import os

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .config import settings

#DATABASE_URL = settings.database_url
#print(DATABASE_URL)

#DATABASE_URL = "sqlite:///./test.db"

#engine = create_async_engine(DATABASE_URL, echo=True, future=True)
engine = create_async_engine(
        "sqlite+aiosqlite:///sql.db",
        echo=True,
    )

async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session