from httpx import AsyncClient
from pytest import Session
import pytest

from models.electricidad import Electricidad

@pytest.mark.asyncio
async def test_get_all_electricidad(async_client: AsyncClient):
    response = await async_client.get("/electricidad/getAll")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_electricidad(async_client: AsyncClient, db_session: Session):

    #Arrange
    new = Electricidad(id_mes=5, monto=123.5, nro_factura="ABCF123")

    #Act
    db_session.add(new)
    await db_session.commit()
    await db_session.refresh(new)
    res = await async_client.get(f'/electricidad/get/{new.id_electricidad}')
    data = res.json()

    #Assert
    assert data['id_mes'] == 5
    assert data['monto'] == 123.5
    assert data['nro_factura'] == 'ABCF123'