from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.especialidades import Especialidades
from typing import List, Optional

class EspecialidadesRepo:

    def __init__(self, db: AsyncSession): 
        self._db = db
        
    async def get_all_especialidades(self)-> List[Especialidades]:
        res = await self._db.execute(select(Especialidades).execution_options(identity_token="no_tracking"))
        return res.scalars().all()

    async def get_especialidad(self, id:int)-> Optional[Especialidades]:
        query = select(Especialidades).filter(Especialidades.sigla_especialidad == id)
        res = await self._db.execute(query)
        return res.scalars().first()

    async def get_especialidad_by_sigla(self, sigla:str)-> Optional[Especialidades]:
        query = select(Especialidades).filter(Especialidades.sigla_especialidad == sigla)
        res = await self._db.execute(query)
        return res.scalars().first()
    
    async def create_especialidad(self, especialidad:Especialidades)-> Especialidades:
        self._db.add(especialidad)
        await self._db.commit()
        await self._db.refresh(especialidad)
        return especialidad