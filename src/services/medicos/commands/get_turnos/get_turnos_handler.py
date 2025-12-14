from fastapi import Depends
from db.db import get_db
from db.entities.turnos import Turnos
from services.medicos.commands.get_medico.get_medico_cmd import GetMedicoCmd
from services.medicos.models.turnos_medico_dto import TurnosMedicosModel
from repository.turnos import TurnosRepo
from sqlalchemy.ext.asyncio import AsyncSession


class GetTurnosHandler():
    def __init__(self, db: AsyncSession): 
        self.__turnos_repo = TurnosRepo(db)
        
    async def handle(self, cmd: GetMedicoCmd) -> list[TurnosMedicosModel]: 
        turnos: list[Turnos] = await self.__turnos_repo.get_turnos_by_medico(cmd.id_medico, True)
        
        res: list[TurnosMedicosModel] = []
        
        for turno in turnos:
            dto = TurnosMedicosModel(
                id_medico=cmd.id_medico, 
                hora_entrada=turno.hora_entrada, 
                hora_salida=turno.hora_salida,
                completado_exitosamente=turno.completado_exitosamente
                )
            
            res.append(dto)
            
        return res
            
            