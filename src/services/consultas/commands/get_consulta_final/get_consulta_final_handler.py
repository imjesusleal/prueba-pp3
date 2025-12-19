from pydantic import BaseModel
from repository.consultas import ConsultasRepo
from db.entities.consultas import Consulta
from services.consultas.commands.get_consulta_final.get_consulta_final_cmd import GetConsultaFinalCmd
from sqlalchemy.ext.asyncio import AsyncSession

from services.consultas.models.consultas_model import ConsultasModel


class GetConsultaFinalHandler:
    def __init__(self, db: AsyncSession):
        self._db = db
        self._repo = ConsultasRepo(db)
        
    async def handle(self, cmd: GetConsultaFinalCmd) -> ConsultasModel | None:
        data: Consulta = await self._repo.get_consulta_by_turno(cmd.id_turno)
        
        if data is None:
            raise ConsultaNotFoundError('La consulta enviada no ha sido encontrada. ', 404)
    
        return ConsultasModel(
            id_turno=data.id_turno,
            id_consulta=data.id_consulta,
            id_medico=data.c_turnos.t_medicos.id_medico,
            medico_nombre=f"{data.c_turnos.t_medicos.nombre} {data.c_turnos.t_medicos.apellido}",
            id_paciente=data.c_turnos.t_paciente.id_pacientes,
            paciente_nombre=f"{data.c_turnos.t_paciente.nombre} {data.c_turnos.t_paciente.apellido}",
            diagnostico=data.diagnostico,
            descripcion=data.descripcion,
            fecha_consulta=data.created_at
        )
        
            
        
    
    