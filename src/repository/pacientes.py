from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.pacientes import Pacientes
from typing import List, Optional

class PacienteRepo: 
    
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_all_pacientes(self) -> List[Pacientes]:
        res = await self._db.execute(select(Pacientes))
        return res.scalars().all()

    async def get_paciente(self,id: int) -> Optional[Pacientes]:
        query = select(Pacientes).filter(Pacientes.id_pacientes == id)
        res = await self._db.execute(query)
        return res.scalars().first()

    async def get_paciente_by_user(self,id_user: int) -> Optional[Pacientes]:
        query = select(Pacientes).filter(Pacientes.id_user == id_user)
        res = await self._db.execute(query)
        return res.scalars().first()

    async def delete_paciente(self,paciente: Pacientes) -> None:
        await self._db.delete(paciente)