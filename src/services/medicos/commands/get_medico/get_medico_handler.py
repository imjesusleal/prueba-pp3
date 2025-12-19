from datetime import datetime
from typing import Optional
from fastapi import Depends
from db.db import get_db
from db.entities.medicos import Medicos
from errors.medicos.medico_not_found import MedicoNotFound
from repository.medicos import MedicosRepo
from sqlalchemy.ext.asyncio import AsyncSession

from services.medicos.commands.get_medico.get_medico_cmd import GetMedicoCmd
from services.medicos.mappers.medicos_mapper import MedicosMapper
from services.medicos.models.get_medico_dto import GetMedidoDto
from services.medicos.services.calculate_rating_service import CalculateRatingService


class GetMedicoHandler():
    def __init__(self, db: AsyncSession):
        self.__repo = MedicosRepo(db)
        self._rating_service = CalculateRatingService()
        
    async def handle(self, cmd: GetMedicoCmd) -> GetMedidoDto:
        medico_data: Optional[Medicos] = await self.__repo.get_medico(cmd.id_medico, True, True, True, True)
        
        if not medico_data:
            raise MedicoNotFound(f"No se ha encontrado el medico con el identificador: {cmd.id_medico}", 404)
        
        
        rating = self._rating_service.calculate_rating(medico_data.m_reviews)
        reviews = len(medico_data.m_reviews)
        atenciones = len(medico_data.m_turnos)
        
        turnos_pendientes = 0
        
        for i in medico_data.m_turnos:
            if i.t_estado.id_turnos_opciones == 2:
                turnos_pendientes += 1



        return MedicosMapper.map_to_dto(medico_data, rating, reviews, atenciones, turnos_pendientes)
        
        
        