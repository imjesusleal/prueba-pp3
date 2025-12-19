from typing import TYPE_CHECKING
from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime

from enums.turnos_opciones import TurnosOpcionesEnums


if TYPE_CHECKING:
    from turnos import Turnos

class EstadosTurnos(SQLModel, table=True):
    __tablename__ = "estados_turnos"
    
    id_estado_turno: int = Field(default=None, primary_key=True)
    id_turno: int = Field(foreign_key="turnos.id_turno", ondelete="CASCADE")
    id_turnos_opciones: int = Field(foreign_key="estados_turnos_opciones.id_turnos_opciones", ondelete="CASCADE")
    created_at: datetime | None = Field(default=None)
    modified_at: datetime | None = Field(default=None)
    
    e_turnos: "Turnos" = Relationship(back_populates="t_estado", sa_relationship_kwargs={"uselist": False})
    
    
    @staticmethod
    def create() -> "EstadosTurnos":
        return EstadosTurnos(
            id_turnos_opciones=2,
            created_at = datetime.now(),
            modified_at = datetime.now()
        ) 

    
    def modificar_estado(self, estado: TurnosOpcionesEnums, clasificacion: int = None):
        self.id_turnos_opciones = estado.value
        self.modified_at = datetime.now()
        self.clasificacion = clasificacion
        
