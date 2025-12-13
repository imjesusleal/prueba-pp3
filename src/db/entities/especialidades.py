from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Especialidades(SQLModel, table=True):
    __tablename__ = "especialidades"

    id_especialidad: int = Field(default=None, primary_key=True)
    sigla_especialidad: str = Field(max_length=5, unique=True)
    descripcion: str = Field()
    created_at: datetime | None = Field(default=None)
    modified_at: datetime | None = Field(default=None)
    
    
    @staticmethod
    def create(sigla_especialidad: str, descripcion: str) -> "Especialidades":
        especialidad = Especialidades(
            sigla_especialidad=sigla_especialidad,
            descripcion=descripcion,
            created_at=datetime.utcnow(),
            modified_at=datetime.utcnow()
        )
        return especialidad 