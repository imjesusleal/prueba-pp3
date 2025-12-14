from datetime import datetime
from pydantic import BaseModel


class TurnosMedicosModel(BaseModel):
    id_medico: int
    hora_entrada: datetime
    hora_salida: datetime
    completado_exitosamente: bool