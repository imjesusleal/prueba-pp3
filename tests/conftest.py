import pytest_asyncio

from httpx import ASGITransport, AsyncClient
from db.db import *
from db.entities import *
from db.entities.users_roles import UsersRoles
from main import app


import pytest
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
TEST_DATABASE_URL_SYNC = "sqlite:///./test.db"

engine_test = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
engine_test_sync = create_engine(TEST_DATABASE_URL_SYNC, echo=False, future=True)

async_session = sessionmaker(
    engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def override_get_db():
    async with async_session() as session:
        yield session
        
app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(autouse=True, scope="session")
async def setup_db():
    # usar SYNC engine para create_all
    SQLModel.metadata.create_all(engine_test_sync)
    yield
    SQLModel.metadata.drop_all(engine_test_sync)
    
    
@pytest_asyncio.fixture(scope="class")
async def db():
    async for s in override_get_db():
        yield s


@pytest_asyncio.fixture(scope="class")
async def seed_roles(db):
    await db.execute(
        UsersRoles.__table__.insert(),
        [
            {"id_users_roles": 1, "rol": "A","description": "Admin"},
            {"id_users_roles": 2, "rol": "M","description": "Medicos"},
            {"id_users_roles": 3, "rol": "P","description": "Pacientes"}
        ]
    )
    await db.commit()


@pytest_asyncio.fixture(scope="class")
async def async_client():
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac