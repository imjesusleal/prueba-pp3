from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.pacientes import Pacientes
from typing import List, Optional


async def get_all_pacientes(db: AsyncSession= Depends(get_db)) -> List[Pacientes]:
    res = await db.execute(select(Pacientes))
    return res.scalars().all()

async def get_paciente(id: int, db: AsyncSession= Depends(get_db)) -> Optional[Pacientes]:
    query = select(Pacientes).filter(Pacientes.id_pacientes == id)
    res = await db.execute(query)
    return res.scalars().first()

async def get_paciente_by_user(id_user: int, db: AsyncSession= Depends(get_db)) -> Optional[Pacientes]:
    query = select(Pacientes).filter(Pacientes.id_user == id_user)
    res = await db.execute(query)
    return res.scalars().first()

async def get_paciente_by_matricula(matricula: str, db: AsyncSession= Depends(get_db)) -> Optional[Pacientes]:
    query = select(Pacientes).filter(Pacientes.matricula == matricula)
    res = await db.execute(query)
    return res.scalars().first()