
from fastapi import Depends
from db.db import get_db
from db.entities.medicos import Medicos
from repository.medicos import MedicosRepo
from services.medicos.commands.get_all.get_medicos_cmd import GetAllMedicosCmd
from sqlalchemy.ext.asyncio import AsyncSession

from services.medicos.mappers.medicos_mapper import MedicosMapper
from services.medicos.models.get_all_medicos_dto import GetAllMedicosDto
from services.medicos.services.calculate_rating_service import CalculateRatingService

class GetAllMedicosCmdHandler:
    def __init__(self, db: AsyncSession):
        self.__medico_repository = MedicosRepo(db)
        self.__calculate_rating_service = CalculateRatingService()
        
    async def handle(self, cmd: GetAllMedicosCmd) -> list[GetAllMedicosDto]:
        data: list[Medicos] = await self.__medico_repository.get_all_medicos_paginated(cmd)
        
        res: list[GetAllMedicosDto] = []
        
        for medico in data:
            rating = self.__calculate_rating_service.calculate_rating(medico.m_reviews)
            reviews = len(medico.m_reviews)
            res.append(MedicosMapper.map_to_grid_model(medico, rating, reviews)) 
        
        return [i for i in res if i.rating >= cmd.clasificacion]
        
        