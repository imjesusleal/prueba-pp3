from fastapi import Depends
from db.db import get_db
from db.entities.especialidades import Especialidades
from errors.especialidades.not_created_error import EspecialidadNotCreatedError
from repository.especialidades import EspecialidadesRepo
from services.especialidades.commands.create_especialidad_cmd import CreateEspecialidadCmd
from sqlalchemy.ext.asyncio import AsyncSession


class CreateEspecialidadHandler:
    def __init__(self, db: AsyncSession):
        self.especialidad_repo = EspecialidadesRepo(db)
        
    async def handle(self, cmd: CreateEspecialidadCmd):
        especialidad = Especialidades.create(cmd.sigla_especialidad, cmd.descripcion) 
        new_especialidad = await self.especialidad_repo.create_especialidad(especialidad)
        
        if not new_especialidad:
            raise EspecialidadNotCreatedError("Ups, ocurrio un error generando la especialiad. ", 500)
        