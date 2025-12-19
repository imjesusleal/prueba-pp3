from typing import TYPE_CHECKING
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime

if TYPE_CHECKING:
    from turnos import Turnos


class Consulta(SQLModel, table=True):
    __tablename__ = "consultas"

    id_consulta: int | None = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True)
    )

    id_turno: int = Field(
        sa_column=Column(Integer, ForeignKey("turnos.id_turno", ondelete="Cascade"), unique=True, nullable=False))

    diagnostico: str | None = Field(
        default=None,
        sa_column=Column(String, nullable=True)
    )

    descripcion: str | None = Field(
        default=None,
        sa_column=Column(String, nullable=True)
    )

    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime, nullable=True)
    )

    modified_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime, nullable=True)
    )
    
    c_turnos: "Turnos" = Relationship(back_populates="t_consultas")
    
    @staticmethod
    def create(id_turno: int, diagnostico: str = None, descripcion: str = None) -> "Consulta":
        return Consulta(
            id_turno=id_turno,
            descripcion=descripcion,
            diagnostico=diagnostico,
            created_at=datetime.now(),
            modified_at=datetime.now()
        )