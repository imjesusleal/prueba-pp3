from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"driver": "ODBC Driver 17 for SQL Server"},
    pool_size=10,
    max_overflow=20,
    future=True,
)

async_sessionmaker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with async_sessionmaker() as session:
        yield session