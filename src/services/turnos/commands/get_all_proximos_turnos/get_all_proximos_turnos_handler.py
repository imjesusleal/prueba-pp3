from db.entities.turnos import Turnos
from enums.turnos_opciones import TurnosOpcionesEnums
from services.turnos.commands.get_all_proximos_turnos.get_all_proximos_turnos_cmd import GetAllProximosTurnosCmd
from services.turnos.mappers.turnos_mapper import MapperTurnos
from services.turnos.models.historial_paciente import HistorialPacienteModel
from repository.turnos import TurnosRepo
from sqlalchemy.ext.asyncio import AsyncSession

class GetAllProximosTurnosHandler:
    __TURNOS_FINALIZADOS = [TurnosOpcionesEnums.Pe]
    
    def __init__(self, db: AsyncSession):
        self._repo = TurnosRepo(db)
    
    async def handle(self, cmd: GetAllProximosTurnosCmd) -> list[HistorialPacienteModel]:
        data: list[Turnos] = await self._repo.get_all_turnos_pacientes(cmd.id_paciente)
        
        turnos_terminados : list[Turnos] = [turno for turno in data if turno.t_estado.id_turnos_opciones in self.__TURNOS_FINALIZADOS]
    
        res: list[HistorialPacienteModel] = []
    
        for turno in turnos_terminados:
            fecha_turno = turno.hora_entrada
            dto = MapperTurnos.map_to_historial_pacientes(turno.id_turno,
                                                          turno.t_medicos.nombre, 
                                                          turno.t_medicos.apellido, 
                                                          turno.t_medicos.m_especialidad.descripcion,
                                                          fecha_turno,
                                                          turno.clasificacion,
                                                          turno.t_consultas.descripcion if turno.t_consultas else '',
                                                          turno.t_estado.id_turnos_opciones
                                                          )
            
            
            res.append(dto)
            
        return res