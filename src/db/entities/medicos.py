from typing import TYPE_CHECKING
from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime

from models.profiles.medifco_profile import MedicoProfile
from services.profiles.medicos.commands.updt_medico_command import UpdtMedicoCommand

if TYPE_CHECKING:
    from users import Users
    from especialidades import Especialidades
    from reviews import Reviews
    from turnos import Turnos

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
    img_name: str = Field(default=None, nullable=True)

    user: "Users"  = Relationship(back_populates="medico", sa_relationship_kwargs={"uselist": False})
    m_especialidad: "Especialidades" = Relationship(sa_relationship_kwargs={"uselist": False})
    m_reviews: list["Reviews"] = Relationship(back_populates="r_medicos")
    m_turnos: list["Turnos"] = Relationship(back_populates="t_medicos")


    def update_self(self, cmd: UpdtMedicoCommand):
        self.matricula = cmd.matricula
        self.telefono = cmd.telefono
        self.modified_at = datetime.now()

    def map_to_model(self) -> MedicoProfile:
        return MedicoProfile(
            nombre= self.nombre,
            apellido = self.apellido,
            id_medico=self.id_medico,
            id_user=self.id_user,
            documento_identificativo=self.documento_identificacion,
            especialidad=self.especialidad,
            matricula=self.matricula,
            telefono=self.telefono,
            img_name=self.img_name
            )
