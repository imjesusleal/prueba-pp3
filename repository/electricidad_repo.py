from fastapi import Depends
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import db, get_db
from models.electricidad import Electricidad


async def get_all(db: AsyncSession) -> list[Electricidad]:
    res = await db.execute(select(Electricidad))
    return res.scalars().all()

async def get(id: int, db: AsyncSession) -> Electricidad: 
    query = select(Electricidad).filter(Electricidad.id_electricidad == id)
    res = await db.execute(query)
    return res.scalars().first()