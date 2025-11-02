from typing import TYPE_CHECKING, ClassVar
from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime

from models.profiles.medifco_profile import MedicoProfile
# from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from users import Users

class Medicos(SQLModel, table=True):
    __tablename__ = "medicos"

    id_medico: int = Field(default=None, primary_key=True)
    id_user: int = Field(unique=True, foreign_key="users.id_user", ondelete="CASCADE")
    documento_identificacion: int = Field(unique=True, foreign_key="documento_identificativo.id_documento")
    nombre: str = Field(max_length=50)
    apellido: str = Field(max_length=50)
    especialidad: int = Field(unique=True, foreign_key="especialidades.id_especialidad")
    matricula: str = Field(max_length=200, unique=True)
    create_at: datetime | None = Field(default=None)
    modified_at: datetime | None = Field(default=None)
    telefono: str | None = Field(default=None)

    user: "Users"  = Relationship(back_populates="medico", sa_relationship_kwargs={"uselist": False})


    def map_to_model(self) -> MedicoProfile:
        return MedicoProfile(
            nombre= self.nombre,
            apellido = self.apellido,
            id_medico=self.id_medico,
            id_user=self.id_user,
            documento_identificativo=self.documento_identificacion,
            especialidad=self.especialidad,
            matricula=self.matricula,
            telefono=self.telefono
            )
