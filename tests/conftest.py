"""
Razón técnica: pytest-asyncio necesita saber qué backend asíncrono usar (asyncio, trio, etc.). Sin configurarlo, obtendrás warnings o errores al ejecutar tests async.
"""
import pytest

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

