from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Medicos(SQLModel, table=True):
    __tablename__ = "medicos"

    id_medico: int = Field(default=None, primary_key=True)
    id_user: int = Field(unique=True, foreign_key="users.id_user")
    documento_identificacion: int = Field(unique=True, foreign_key="documento_identificativo.id_documento")
    especialidad: int = Field(unique=True, foreign_key="especialidades.id_especialidad")
    matricula: str = Field(max_length=200, unique=True)
    create_at: datetime | None = Field(default=None)
    modified_at: datetime | None = Field(default=None)
    telefono: str | None = Field(default=None)