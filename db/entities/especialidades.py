from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Especialidades(SQLModel, table=True):
    __tablename__ = "especialidades"

    id_especialidad: Optional[int] = Field(default=None, primary_key=True)
    sigla_especialidad: str = Field(max_length=5, unique=True)
    descripcion: str = Field()
    created_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)