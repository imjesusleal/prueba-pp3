from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.reviews import Reviews
from typing import List, Optional

async def get_all_reviews(db: AsyncSession = Depends(get_db)) -> List[Reviews]:
    res = await db.execute(select(Reviews))
    return res.scalars().all()

async def get_review(id: int, db: AsyncSession = Depends(get_db)) -> Optional[Reviews]:
    query = select(Reviews).filter(Reviews.id_review == id)
    res = await db.execute(query)
    return res.scalars().first()

async def get_reviews_by_medico(id_medico: int, db: AsyncSession= Depends(get_db)) -> List[Reviews]:
    query = select(Reviews).filter(Reviews.id_medico == id_medico)
    res = await db.execute(query)
    return res.scalars().all()

async def get_reviews_by_paciente(id_paciente: int, db: AsyncSession = Depends(get_db)) -> List[Reviews]:
    query = select(Reviews).filter(Reviews.id_paciente == id_paciente)
    res = await db.execute(query)
    return res.scalars().all()

async def get_reviews_by_calificacion(calificacion: int, db: AsyncSession = Depends(get_db)) -> List[Reviews]:
    query = select(Reviews).filter(Reviews.calificacion == calificacion)
    res = await db.execute(query)
    return res.scalars().all()