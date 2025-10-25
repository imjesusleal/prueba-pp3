from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Consultas(SQLModel, table=True):
    __tablename__ = "consultas"
    
    id_consulta: Optional[int] = Field(default=None, primary_key=True)
    id_turno: int = Field(unique=True, foreign_key="turnos.id_turno")
    diagnostico: Optional[str] = Field(default=None)
    descripcion: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)