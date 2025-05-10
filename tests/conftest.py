
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from main import app
from db.db import db, get_db  
DATABASE_TEST_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(DATABASE_TEST_URL, echo=False)
TestingSessionLocal = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(db.metadata.create_all)
    app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client: 
        yield client