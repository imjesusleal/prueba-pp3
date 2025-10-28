from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Reviews(SQLModel, table=True):
    __tablename__ = "reviews"
    
    id_review: int = Field(primary_key=True)
    id_medico: int = Field(foreign_key="medicos.id_medico")
    id_paciente: int = Field(foreign_key="pacientes.id_pacientes")
    calificacion: int | None = Field()
    comentario: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    modified_at: datetime | None = Field(default=None)