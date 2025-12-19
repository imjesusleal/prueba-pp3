from datetime import datetime
from pydantic import BaseModel


class ConsultasModel(BaseModel):
    id_turno: int   
    id_consulta: int
    id_medico: int
    medico_nombre: str
    id_paciente: int
    paciente_nombre: str
    diagnostico: str
    descripcion: str
    fecha_consulta: datetime