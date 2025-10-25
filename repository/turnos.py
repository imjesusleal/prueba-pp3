from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.turnos import Turnos
from typing import List, Optional

async def get_all_turnos(db: AsyncSession= Depends(get_db)) -> List[Turnos]:#Es necesario que llame primero a todos los turnos
    res = await db.execute(select(Turnos))
    return res.scalars().all()

async def get_turno(id: int, db: AsyncSession= Depends(get_db)) -> Optional[Turnos]:
    query = select(Turnos).filter(Turnos.id_turno == id)
    res = await db.execute(query)
    return res.scalars().first()

async def get_turnos_by_medico(id_medico: int, db: AsyncSession= Depends(get_db)) -> List[Turnos]:
    query = select(Turnos).filter(Turnos.id_medico == id_medico)
    res = await db.execute(query)
    return res.scalars().all()

async def get_turnos_by_paciente(id_paciente: int, db: AsyncSession= Depends(get_db)) -> List[Turnos]:#bsuqueda por turnos que hace el paciente
    query = select(Turnos).filter(Turnos.id_paciente == id_paciente)
    res = await db.execute(query)
    return res.scalars().all()

async def get_turnos_completados(db: AsyncSession= Depends(get_db)) -> List[Turnos]:#turno ya completados, filtro
    query = select(Turnos).filter(Turnos.completado_exitosamente == True)
    res = await db.execute(query)
    return res.scalars().all()

async def get_turnos_pendientes(db: AsyncSession= Depends(get_db)) -> List[Turnos]:
    query = select(Turnos).filter(Turnos.completado_exitosamente == False)
    res = await db.execute(query)
    return res.scalars().all()