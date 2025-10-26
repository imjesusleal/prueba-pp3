from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.users import Users
from typing import Optional

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