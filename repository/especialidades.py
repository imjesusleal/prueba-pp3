from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.especialidades import Especialidades
from typing import List, Optional


async def get_all_especialidades(db:AsyncSession = Depends(get_db))-> List[Especialidades]:
    res = await db.execute(select(Especialidades))
    return res.scalars().all()

async def get_especialidad(id:int, db:AsyncSession= Depends(get_db))-> Optional[Especialidades]:
    query = select(Especialidades).filter(Especialidades.sigla_especialidad == id)
    res = await db.execute(query)
    return res.scalars().first()

async def get_especialidad_by_sigla(sigla:str, db:AsyncSession= Depends(get_db))-> Optional[Especialidades]:
    query = select(Especialidades).filter(Especialidades.sigla_especialidad == sigla)
    res = await db.execute(query)
    return res.scalars().first()