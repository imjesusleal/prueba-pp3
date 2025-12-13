from fastapi import Depends
from db.db import get_db
from db.entities.especialidades import Especialidades
from repository.especialidades import EspecialidadesRepo
from sqlalchemy.ext.asyncio import AsyncSession
from services.especialidades.models.especialidades_dto import EspecialidadesDto

class GetAllEspecialidadesHandler:
    def __init__(self):
        self.__especialidades_repository = EspecialidadesRepo() 
    
    
    async def handle(self, db: AsyncSession = Depends(get_db)) -> list[EspecialidadesDto]:
        data: list[Especialidades] = await self.__especialidades_repository.get_all_especialidades(db)
        
        res: list[EspecialidadesDto] = []
        
        for especialidad in data:
            dto = EspecialidadesDto(
                id_especialidad=especialidad.id_especialidad,
                sigla_especialidad=especialidad.sigla_especialidad,
                descripcion=especialidad.descripcion
            )
            
            res.append(dto)   
        
        return res