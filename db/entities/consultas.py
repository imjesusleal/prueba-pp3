from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlmodel import SQLModel, Field
from datetime import datetime


class Consulta(SQLModel, table=True):
    __tablename__ = "consultas"

    id_consulta: int | None = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True)
    )

    id_turno: int = Field(
        sa_column=Column(Integer, ForeignKey("turnos.id_turno"), unique=True, nullable=False)
    )

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