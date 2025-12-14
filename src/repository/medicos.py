from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.entities.medicos import Medicos
from typing import List, Optional
from sqlalchemy.orm import  joinedload

from services.medicos.commands.get_all.get_medicos_cmd import GetAllMedicosCmd

class MedicosRepo:
    
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_all_medicos(self) -> List[Medicos]:
        res = await self._db.execute(select(Medicos))
        return res.scalars().all()

    async def get_all_medicos_paginated(self,cmd: GetAllMedicosCmd) -> List[Medicos]:
        query = select(Medicos).options(joinedload(Medicos.m_especialidad), joinedload(Medicos.m_reviews)).execution_options(identity_token="no_tracking")
        
        if cmd.especialidad:
            query = query.filter(Medicos.especialidad == cmd.especialidad)
        
        if cmd.cursor_id:
            query = query.filter(Medicos.id_medico > cmd.cursor_id)
              
        query = query.limit(cmd.limit)
        
        res = await self._db.execute(query)
        return res.unique().scalars().all()
        

    async def get_medico(self,id: int, include_especialidad: bool = False, include_reviews: bool = False, include_turnos: bool = False, as_no_track: bool = False) -> Optional[Medicos]:
        query = select(Medicos).filter(Medicos.id_medico == id)
        
        if include_especialidad:
            query = query.options(joinedload(Medicos.m_especialidad))
        
        if include_reviews:
            query = query.options(joinedload(Medicos.m_reviews))
            
        if include_turnos:
            query = query.options(joinedload(Medicos.m_turnos))
            
        if as_no_track:
            query = query.execution_options(identity_token="no_tracking")
            
        res = await self._db.execute(query)
        return res.unique().scalars().first()

    async def get_medico_by_user(self,id_user: int, no_tracking = False) -> Optional[Medicos]:#conecta un perfil usuario con un perfil medico
        query = select(Medicos) 
        if (no_tracking):
            query = query.filter(Medicos.id_user == id_user).execution_options(identity_token = "no_tracking")
        else:
            query = query.filter(Medicos.id_user == id_user)
        res = await self._db.execute(query)
        return res.scalars().first()

    async def get_medico_by_matricula(self,matricula: str) -> Optional[Medicos]:#busca un medico por su matricula
        query = select(Medicos).filter(Medicos.matricula == matricula)
        res = await self._db.execute(query)
        return res.scalars().first()

    async def get_medicos_by_especialidad(self,especialidad_id: int) -> List[Medicos]:#busca por especialidad
        query = select(Medicos).filter(Medicos.especialidad == especialidad_id)
        res = await self._db.execute(query)
        return res.scalars().all()
    
    async def delete_medico(self,medico: Medicos) -> None:
        await self._db.delete(medico)
