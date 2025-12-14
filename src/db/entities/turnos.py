from typing import TYPE_CHECKING
from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime

if TYPE_CHECKING:
    from medicos import Medicos

class Turnos(SQLModel, table=True):
    __tablename__ = "turnos"
    
    id_turno: int = Field(default=None, primary_key=True)
    id_medico: int = Field(foreign_key="medicos.id_medico", ondelete="CASCADE")
    id_paciente: int = Field(foreign_key="pacientes.id_pacientes")
    hora_entrada: datetime = Field()
    hora_salida: datetime = Field()
    completado_exitosamente: bool = Field()
    created_at: datetime | None = Field(default=None)
    modified_at: datetime | None = Field(default=None)
    
    t_medicos: "Medicos" = Relationship(back_populates="m_turnos", sa_relationship_kwargs={"uselist": False})
    
    
    @staticmethod
    def create(id_medico: int, id_paciente: int, hora_entrada: datetime, hora_salida: datetime) -> "Turnos":
        return Turnos(
            id_medico=id_medico,
            id_paciente=id_paciente,
            hora_entrada=hora_entrada,
            hora_salida=hora_salida,
            completado_exitosamente=False,
            created_at=datetime.now(),
            modified_at=datetime.now()
        )