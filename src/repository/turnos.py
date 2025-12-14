from datetime import datetime
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.entities.turnos import Turnos
from typing import List, Optional

class TurnosRepo:
    
    def __init__(self, db: AsyncSession):
        self._db = db
    
    async def get_all_turnos(self) -> List[Turnos]:
        res = await self._db.execute(select(Turnos))
        return res.scalars().all()

    async def get_turno(self,id: int) -> Optional[Turnos]:
        query = select(Turnos).filter(Turnos.id_turno == id)
        res = await self._db.execute(query)
        return res.scalars().first()
    
    async def get_turno_between_fecha(self,hora_entrada: datetime, hora_salida: datetime, as_no_track: bool = False)-> Optional[Turnos]:
        query = select(Turnos).where((Turnos.hora_entrada >= hora_entrada) & (Turnos.hora_salida <= hora_salida))
        
        if as_no_track:
            query = query.execution_options(identity_token="no_tracking")
            
        res = await self._db.execute(query)
        return res.scalar()
    
    async def get_turnos_by_medico(self,id_medico: int, as_no_tracking = False) -> List[Turnos]:
        query = select(Turnos).filter(Turnos.id_medico == id_medico)
        
        if as_no_tracking:
            query = query.execution_options(identity_token="no_tracking")
        
        res = await self._db.execute(query)
        return res.scalars().all()
    
    def add(self,turno: Turnos) -> None:
        self._db.add(turno)

    async def get_turnos_by_paciente(self,id_paciente: int) -> List[Turnos]:
        query = select(Turnos).filter(Turnos.id_paciente == id_paciente)
        res = await self._db.execute(query)
        return res.scalars().all()

    async def get_turnos_completados(self) -> List[Turnos]:
        query = select(Turnos).filter(Turnos.completado_exitosamente == True)
        res = await self._db.execute(query)
        return res.scalars().all()

    async def get_turnos_pendientes(self) -> List[Turnos]:
        query = select(Turnos).filter(Turnos.completado_exitosamente == False)
        res = await self._db.execute(query)
        return res.scalars().all()