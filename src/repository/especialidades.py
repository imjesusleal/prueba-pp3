from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.especialidades import Especialidades
from typing import List, Optional

class EspecialidadesRepo:

    async def get_all_especialidades(self, db:AsyncSession = Depends(get_db))-> List[Especialidades]:
        res = await db.execute(select(Especialidades).execution_options(identity_token="no_tracking"))
        return res.scalars().all()

    async def get_especialidad(self, id:int, db:AsyncSession= Depends(get_db))-> Optional[Especialidades]:
        query = select(Especialidades).filter(Especialidades.sigla_especialidad == id)
        res = await db.execute(query)
        return res.scalars().first()

    async def get_especialidad_by_sigla(self, sigla:str, db:AsyncSession= Depends(get_db))-> Optional[Especialidades]:
        query = select(Especialidades).filter(Especialidades.sigla_especialidad == sigla)
        res = await db.execute(query)
        return res.scalars().first()
    
    async def create_especialidad(self, especialidad:Especialidades, db:AsyncSession= Depends(get_db))-> Especialidades:
        db.add(especialidad)
        await db.commit()
        await db.refresh(especialidad)
        return especialidad