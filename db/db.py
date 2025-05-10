from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class DbCtx(): 
    def __init__(self):
        self.__database_url = DATABASE_URL
        self.engine = create_async_engine(self.__database_url, echo=True)
        self._sessionmaker = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)

    @asynccontextmanager
    async def session(self):
        async with self._sessionmaker() as session:
            yield session
        

    @property
    def metadata(self):
        return SQLModel.metadata
    
    
db = DbCtx()

async def get_db():
    async with db.session() as session:
        yield session