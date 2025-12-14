from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.users import Users
from db.entities.users_roles import UsersRoles
from typing import List, Optional


class UsersRolesRepository: 

    def __init__(self, db: AsyncSession): 
        self._db = db

    async def get_all_users_roles(self) -> List[UsersRoles]:
        res = await self._db.execute(select(UsersRoles))
        #es equivalente a escribir en SQL: SELECT * FROM users_roles/db.execute se consulta a la BD y se espera la respuesta en el 'res'
        return res.scalars().all()#lo devuelve en una lista

    async def get_user_role(self,id: int) -> Optional[UsersRoles]:
        query = select(UsersRoles).filter(UsersRoles.id_users_roles == id)
        res = await self._db.execute(query)
        return res.scalars().first()

    async def get_user_role_by_rol(self,rol: str) -> Optional[UsersRoles]:
        query = select(UsersRoles).filter(UsersRoles.rol == rol)
        res = await self._db.execute(query)
        return res.scalars().first()
    