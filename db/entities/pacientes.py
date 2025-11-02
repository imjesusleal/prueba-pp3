from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Pacientes(SQLModel, table=True):
    __tablename__ = "pacientes"

    id_pacientes: int = Field(default=None, primary_key=True)
    id_user: int = Field(unique=True, foreign_key="users.id_user", ondelete="CASCADE")
    documento_identificacion: int = Field(unique=True, foreign_key="documento_identificativo.id_documento")
    nombre: str = Field(max_length=50)
    apellido: str = Field(max_length=50)
    create_at: datetime | None = Field(default=None)
    modified_at: datetime | None = Field(default=None)