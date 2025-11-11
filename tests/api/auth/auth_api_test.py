from httpx import AsyncClient
from pytest import Session
import pytest

from models.auth_models.user_register import UserRegister
# from models.auth_models.user_login import UserLogin
# from repository.users import UserRepository


# class AuthTest:

@pytest.mark.asyncio
async def test_register_admin(async_client: AsyncClient, db_session: Session):

    #Arrange
    user = UserRegister(username="hola", password="hola2", email="hola@hola.com", user_rol=1)
    #Act
    await db_session.commit()
    await db_session.refresh(user)
    res = await async_client.post(f'api/v1/auth/login', data={"username": user.username, "password": user.password})
    data = res.json()
    #Assert
    assert data