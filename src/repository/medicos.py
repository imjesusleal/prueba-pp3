from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.medicos import Medicos
from typing import List, Optional
from sqlalchemy.orm import selectinload, joinedload

from services.medicos.commands.get_all.get_medicos_cmd import GetAllMedicosCmd

class MedicosRepo:

    async def get_all_medicos(self,db: AsyncSession = Depends(get_db)) -> List[Medicos]:
        res = await db.execute(select(Medicos))
        return res.scalars().all()

    async def get_all_medicos_paginated(self,cmd: GetAllMedicosCmd, db: AsyncSession = Depends(get_db)) -> List[Medicos]:
        query = select(Medicos).options(joinedload(Medicos.m_especialidad), joinedload(Medicos.m_reviews)).execution_options(identity_token="no_tracking")
        
        if cmd.especialidad:
            query = query.filter(Medicos.especialidad == cmd.especialidad)
        
        if cmd.cursor_id:
            query = query.filter(Medicos.id_medico > cmd.cursor_id)
              
        query = query.limit(cmd.limit)
        
        res = await db.execute(query)
        return res.unique().scalars().all()
        

    async def get_medico(self,id: int, db: AsyncSession= Depends(get_db)) -> Optional[Medicos]:
        query = select(Medicos).filter(Medicos.id_medico == id)
        res = await db.execute(query)
        return res.scalars().first()

    async def get_medico_by_user(self,id_user: int, db: AsyncSession= Depends(get_db), no_tracking = False) -> Optional[Medicos]:#conecta un perfil usuario con un perfil medico
        query = select(Medicos) 
        if (no_tracking):
            query = query.filter(Medicos.id_user == id_user).execution_options(identity_token = "no_tracking")
        else:
            query = query.filter(Medicos.id_user == id_user)
        res = await db.execute(query)
        return res.scalars().first()

    async def get_medico_by_matricula(self,matricula: str, db: AsyncSession= Depends(get_db)) -> Optional[Medicos]:#busca un medico por su matricula
        query = select(Medicos).filter(Medicos.matricula == matricula)
        res = await db.execute(query)
        return res.scalars().first()

    async def get_medicos_by_especialidad(self,especialidad_id: int, db: AsyncSession= Depends(get_db)) -> List[Medicos]:#busca por especialidad
        query = select(Medicos).filter(Medicos.especialidad == especialidad_id)
        res = await db.execute(query)
        return res.scalars().all()
    
    async def delete_medico(self,medico: Medicos, db: AsyncSession= Depends(get_db)) -> None:
        await db.delete(medico)
