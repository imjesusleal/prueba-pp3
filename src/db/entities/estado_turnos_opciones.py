from sqlmodel import CHAR, VARCHAR, Column, SQLModel, Field
from datetime import datetime


class EstadoTurnosOpciones(SQLModel, table=True):
    __tablename__ = "estados_turnos_opciones"
    
    id_turnos_opciones: int = Field(default=None, primary_key=True)
    valor: str = Field(sa_column=Column(CHAR(2), nullable=False))
    descripcion: str = Field(sa_column=Column(VARCHAR(100), nullable=False)) 
    created_at: datetime | None = Field(default=None)
    modified_at: datetime | None = Field(default=None)
    