from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Turnos(SQLModel, table=True):
    __tablename__ = "turnos"
    
    id_turno: int = Field(default=None, primary_key=True)
    id_medico: int = Field(foreign_key="medicos.id_medico")
    id_paciente: int = Field(foreign_key="pacientes.id_pacientes")
    hora_entrada: datetime = Field()
    hora_salida: datetime = Field()
    completado_exitosamente: bool = Field()
    created_at: datetime | None = Field(default=None)
    modified_at: datetime | None = Field(default=None)