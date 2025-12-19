from services.turnos.commands.get_all_atenciones_medicas.get_all_atenciones_medicas_cmd import GetAllAtencionesMedicasCmd
from services.turnos.mappers.turnos_mapper import MapperTurnos
from services.turnos.models.historial_atenciones import HistorialAtencionesModel
from repository.turnos import TurnosRepo
from sqlalchemy.ext.asyncio import AsyncSession

class GetAllAtencionesMedicasHandler:
    def __init__(self, db: AsyncSession):
        self._repo = TurnosRepo(db)
        
    async def handle(self, cmd: GetAllAtencionesMedicasCmd) -> list[HistorialAtencionesModel]: 
        turnos_data = await self._repo.get_turnos_completo_by_medico(cmd.id_medico, cmd.estado, True)
        
        res: list[HistorialAtencionesModel] = [] 
        
        for turno in turnos_data:
            res.append(MapperTurnos.map_to_historial_atenciones(
                turno.id_turno,
                turno.id_medico,
                turno.id_paciente,
                turno.t_paciente.nombre,
                turno.t_paciente.apellido,
                turno.hora_entrada,
                turno.t_estado.id_turnos_opciones,
                turno.t_medicos.m_especialidad.descripcion
            ))
            
        return res 