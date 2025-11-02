from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.medicos import Medicos
from db.entities.users import Users
from typing import Optional
from sqlalchemy.orm import selectinload, joinedload

from models.auth_models.user_login import UserLogin

class UserRepository:

    async def get_user(self,  user: UserLogin, db: AsyncSession = Depends(get_db)) -> Optional[Users]:#busca usuarios por su username
        query = select(Users).filter(Users.username == user.username and Users.password == user.password)
        res = await db.execute(query)
        db_user = res.scalars().first()
        return db_user

    async def get_user_by_email(self, email: str, db: AsyncSession = Depends(get_db)) -> Optional[Users]:#busca usuarios por su mail
        query = select(Users).filter(Users.email == email)
        res = await db.execute(query)
        return res.scalars().first()
    
    async def get_user_by_id(self,  user_id: int, db: AsyncSession = Depends(get_db)) -> Optional[Users]:
        """
            Busca el user por id para refrescar el token
        """
        query = select(Users).filter(Users.id_user == user_id)
        res = await db.execute(query)
        db_user = res.scalars().first()
        return db_user
    
    async def get_user_with_medico_profile(self, user_id: int, db: AsyncSession = Depends(get_db)):
        query = select(Users).filter(Users.id_user == user_id).options(joinedload(Users.medico))
        res = await db.execute(query)
        return res.scalars().first()
    