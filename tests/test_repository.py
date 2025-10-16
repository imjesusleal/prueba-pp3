"""Para las pruebas unitarias utilizamos un repositorio mock que viene con la libreria unittest, como indican las buenas prácticas"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from repository.medify_repositories import Users, UserRoles

@pytest.mark.asyncio
async def test_repository_getID():
    #simular el user
    mock_user_model = MagicMock()
    mock_user_model.id_user = 1
    mock_user_model.username = "Fulano"
    #Devolución
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user_model
    mock_session.execute.return_value = mock_result

    repo = Users(session=mock_session)
    resultado = await repo.getID(1)

    assert resultado is not None
    assert resultado.id_user == 1
    assert resultado.username == "Fulano"
