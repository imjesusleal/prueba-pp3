from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from models.profiles.paciente_profile import PacienteProfile
from services.profiles.pacientes.commands.updt_paciente_cmd import UpdtPacienteCommand


if TYPE_CHECKING:
    from users import Users
    from turnos import Turnos

class Pacientes(SQLModel, table=True):
    __tablename__ = "pacientes"

    id_pacientes: int = Field(default=None, primary_key=True)
    id_user: int = Field(unique=True, foreign_key="users.id_user", ondelete="CASCADE")
    documento_identificacion: int = Field(foreign_key="documento_identificativo.id_documento")
    nombre: str = Field(max_length=50)
    apellido: str = Field(max_length=50)
    create_at: datetime | None = Field(default=None)
    modified_at: datetime | None = Field(default=None)
    img_name: str = Field(default=None, nullable=True)

    user: "Users"  = Relationship(back_populates="paciente", sa_relationship_kwargs={"uselist": False})
    p_turnos: "Turnos" = Relationship(back_populates="t_paciente", sa_relationship_kwargs={"uselist": True})

    def map_to_model(self) -> PacienteProfile:
        return PacienteProfile(
            nombre= self.nombre,
            apellido = self.apellido,
            id_user=self.id_user,
            id_paciente=self.id_pacientes,
            documento_identificativo=self.documento_identificacion,
            img_name=self.img_name
            )

    def update_self(self, cmd: UpdtPacienteCommand):
        self.nombre = cmd.nombre
        self.apellido = cmd.apellido
        self.modified_at = datetime.now()