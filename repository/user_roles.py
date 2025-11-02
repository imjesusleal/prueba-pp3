from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.users import Users
from db.entities.users_roles import UsersRoles
from typing import List, Optional


class UsersRolesRepository: 

    async def get_all_users_roles(self,db: AsyncSession = Depends(get_db)) -> List[UsersRoles]:
        res = await db.execute(select(UsersRoles))
        #es equivalente a escribir en SQL: SELECT * FROM users_roles/db.execute se consulta a la BD y se espera la respuesta en el 'res'
        return res.scalars().all()#lo devuelve en una lista

    async def get_user_role(self,id: int, db: AsyncSession = Depends(get_db)) -> Optional[UsersRoles]:
        query = select(UsersRoles).filter(UsersRoles.id_users_roles == id)#se puede traducir como un WHERE
        res = await db.execute(query)
        return res.scalars().first()

    async def get_user_role_by_rol(self,rol: str, db: AsyncSession = Depends(get_db)) -> Optional[UsersRoles]:
        query = select(UsersRoles).filter(UsersRoles.rol == rol)#funciona como un WHERE rol 
        res = await db.execute(query)
        return res.scalars().first()
    