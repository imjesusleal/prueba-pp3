from fastapi import Depends
from sqlalchemy import case, exists
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.consultas import Consulta
from typing import List, Optional
from sqlalchemy.orm import  joinedload

from db.entities.turnos import Turnos

def default_options() -> tuple:
    return (
        joinedload(Consulta.c_turnos)
            .joinedload(Turnos.t_medicos),
        joinedload(Consulta.c_turnos)
            .joinedload(Turnos.t_paciente),
    )

class ConsultasRepo:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_all_consultas(self) -> List[Consulta]:
        res = await self._db.execute(select(Consulta))
        return res.scalars().all()

    async def get_consulta(self, id: int) -> Optional[Consulta]:
        query = select(Consulta).filter(Consulta.id_consulta == id)
        res = await self._db.execute(query)
        return res.scalars().first()

    async def get_consulta_by_turno(self, id_turno: int, as_no_track: bool = False) -> Optional[Consulta]:
        query = select(Consulta).filter(Consulta.id_turno == id_turno).options(*default_options())
        
        if as_no_track: 
            query = query.execution_options(identity_token="no_tracking")
            
        res = await self._db.execute(query)
        return res.scalars().first()
    
    async def existe(self, id_turno: int) -> Optional[Consulta]:
        query = select(
            case(
                (exists().where(Consulta.id_turno == id_turno), True),
                else_=False
            )
        )

        res = await self._db.execute(query)
        return res.scalar()
    
    def add(self, consulta: Consulta):
        self._db.add(consulta)
