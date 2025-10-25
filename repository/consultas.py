from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.consultas import Consultas
from typing import List, Optional



async def get_all_consultas(db: AsyncSession = Depends(get_db)) -> List[Consultas]:
    res = await db.execute(select(Consultas))
    return res.scalars().all()

async def get_consulta(id: int, db: AsyncSession = Depends(get_db)) -> Optional[Consultas]:
    query = select(Consultas).filter(Consultas.id_consulta == id)
    res = await db.execute(query)
    return res.scalars().first()

async def get_consulta_by_turno(id_turno: int, db: AsyncSession = Depends(get_db)) -> Optional[Consultas]:
    query = select(Consultas).filter(Consultas.id_turno == id_turno)
    res = await db.execute(query)
    return res.scalars().first()
