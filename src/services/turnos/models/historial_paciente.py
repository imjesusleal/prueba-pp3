from datetime import datetime
from pydantic import BaseModel


class HistorialPacienteModel(BaseModel):
    id_turno: int
    nombre_medico: str
    apellido_medico: str
    especialidad:str 
    fecha_turno: datetime
    clasificacion: int
    observaciones: str
    estado_turno: str