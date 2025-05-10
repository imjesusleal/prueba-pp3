import pytest
from pytest import Session
from sqlalchemy.ext.asyncio import AsyncSession
from models.electricidad import Electricidad
from services.electricidad_service import get, get_all

@pytest.mark.asyncio
async def test_get_all_service(db_session: Session):
    mock_electricidad = Electricidad(id_mes=3, monto=151, nro_factura="82374223")
    db_session.add(mock_electricidad)

    res = await get_all(db_session)

    print(res[0].id_electricidad)
    print(res[0].id_mes)
    print(res[0].monto)
    print(res[0].nro_factura)
    assert len(res) > 0
