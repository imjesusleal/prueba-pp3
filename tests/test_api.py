import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from api.main import app


@pytest.mark.asyncio
async def test_endpoint_health():
    #Preparancion
    transport = ASGITransport(app=app)#Conexión directa hacia nuestra app
    async with AsyncClient(transport=transport, base_url="http://test") as client:#navegador robot del paquete httpx para hacer peticiones asincrona a HTTP
        #Ejecución
        response = await client.get("/health")
    #verificación

    assert response.status_code == 200 or 201
    assert response.json() == {"status": "ok"}