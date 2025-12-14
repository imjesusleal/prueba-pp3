from ast import List
from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime
from typing import Optional
# from sqlalchemy.orm import relationship, Mapped
from typing import ClassVar

from db.entities.medicos import Medicos
from db.entities.pacientes import Pacientes
from services.profiles.medicos.commands.add_medico_command import AddMedicoCommand
from services.profiles.pacientes.commands.add_paciente_cmd import AddPacienteCmd


class Users(SQLModel, table=True):
    __tablename__= "users"

    id_user: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=100, unique=True)
    password: str = Field(max_length=255)
    email: str = Field(max_length=255, unique=True)
    user_rol: Optional[int] = Field(default=None, foreign_key="users_roles.id_users_roles")
    created_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)

    medico:Medicos = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})
    paciente: Pacientes = Relationship(back_populates="user",  sa_relationship_kwargs={"uselist": False})

    def create_medico(self, cmd: AddMedicoCommand): 
        self.medico = Medicos(
            id_user=cmd.id_user,
            especialidad=cmd.especialidad,
            documento_identificacion=cmd.documento_identificativo,
            telefono=cmd.telefono,
            matricula=cmd.matricula,
            create_at=datetime.now(),
            modified_at=datetime.now(),
            nombre=cmd.nombre,
            apellido=cmd.apellido
            )
        
    def create_paciente(self, cmd: AddPacienteCmd):
        self.paciente = Pacientes(
            id_user = self.id_user,
            nombre= cmd.nombre,
            apellido= cmd.apellido,
            documento_identificacion= cmd.documento_identificativo,
            create_at= datetime.now(),
            updated_at = datetime.now()
        )
        
    def delete_medico(self):
        """
            Esto es una deficiencia mental mia, porque no confío en el repo que arme. Porlas, lo borro también del user y que se joda.
        """
        self.medico = None
    
    def delete_paciente(self):
        """
            Esto es una deficiencia mental mia, porque no confío en el repo que arme. Porlas, lo borro también del user y que se joda.
        """
        self.paciente = None