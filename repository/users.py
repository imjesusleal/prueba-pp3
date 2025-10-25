from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.users import Users
from typing import List, Optional

async def get_all_user(db: AsyncSession = Depends(get_db)) -> List[Users]:#trae todos los usuarios
    res = await db.execute(select(Users))
    return res.scalars().all()

async def get_user(id: int, db: AsyncSession = Depends(get_db)) -> Optional[Users]:#trae a los usuarios por su id
    query = select(Users).filter(Users.id_user == id)
    res = await db.execute(query)
    return res.scalars().first()

async def get_user_by_username(username: str, db: AsyncSession = Depends(get_db)) -> Optional[Users]:#busca usuarios por su username
    query = select(Users).filter(Users.username == username)
    res = await db.execute(query)
    return res.scalars().first()

async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)) -> Optional[Users]:#busca usuarios por su mail
    query = select(Users).filter(Users.email == email)
    res = await db.execute(query)
    return res.scalars().first()