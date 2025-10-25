from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.medicos import Medicos
from typing import List, Optional


async def get_all_medicos(db: AsyncSession = Depends(get_db)) -> List[Medicos]:
    res = await db.execute(select(Medicos))
    return res.scalars().all()

async def get_medico(id: int, db: AsyncSession= Depends(get_db)) -> Optional[Medicos]:
    query = select(Medicos).filter(Medicos.id_medico == id)
    res = await db.execute(query)
    return res.scalars().first()

async def get_medico_by_user(id_user: int, db: AsyncSession= Depends(get_db)) -> Optional[Medicos]:#conecta un perfil usuario con un perfil medico
    query = select(Medicos).filter(Medicos.id_user == id_user)
    res = await db.execute(query)
    return res.scalars().first()

async def get_medico_by_matricula(matricula: str, db: AsyncSession= Depends(get_db)) -> Optional[Medicos]:#busca un medico por su matricula
    query = select(Medicos).filter(Medicos.matricula == matricula)
    res = await db.execute(query)
    return res.scalars().first()

async def get_medicos_by_especialidad(especialidad_id: int, db: AsyncSession= Depends(get_db)) -> List[Medicos]:#busca por especialidad
    query = select(Medicos).filter(Medicos.especialidad == especialidad_id)
    res = await db.execute(query)
    return res.scalars().all()
