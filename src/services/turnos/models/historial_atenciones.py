from datetime import datetime
from pydantic import BaseModel


class HistorialAtencionesModel(BaseModel):
    id_turno:int
    id_medico: int
    id_paciente: int
    nombre_paciente: str
    apellido_paciente: str
    hora_atencion: datetime
    estado: str
    especialidad: str   