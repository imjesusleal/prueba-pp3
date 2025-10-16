from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

"""
Mapeamos el esquema DER,
Agregamos campos opcionales,/https://stackoverflow.com/questions/72720210/python-sqlmodel-optional-id-value-for-auto-increment-causes-type-errors-when-r / https://sqlmodel.tiangolo.com/tutorial/automatic-id-none-refresh/
Aplicación de constrains de unique y foreign keys/https://learn.microsoft.com/en-us/sql/relational-databases/tables/primary-and-foreign-key-constraints?view=sql-server-ver17

"""

class Users(SQLModel, table=True):
    __tablename__= "users"

    id_user: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=100, unique=True)
    password: str = Field(max_length=255)
    email: str = Field(max_length=255, unique=True)
    user_rol: Optional[int] = Field(default=None, foreign_key="users.id_user")
    created_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)

class UserRoles(SQLModel, table=True):
    __tablename__ = "users_roles"
    
    id_users_roles: Optional[int] = Field(default=None, primary_key=True)
    rol: str = Field(max_length=1)
    description: str = Field(max_length=255)
    created_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)

class Especialidades(SQLModel, table=True):
    __tablename__ = "especialidades"

    id_especialidad: Optional[int] = Field(default=None, primary_key=True)
    sigla_especialidad: str = Field(max_length=5, unique=True)
    descripcion: str = Field()
    created_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)

class DocumentoIdentificativo(SQLModel, table=True):
    __tablename__ = "documento_identificativo"

    id_documento: Optional[int] = Field(default=None, primary_key=True)
    tipo_documento: str = Field(max_length=10, unique=True)
    descripcion_documento: str = Field()
    created_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)

class Medicos(SQLModel, table=True):
    __tablename__ = "medicos"

    id_medico: Optional[int] = Field(default=None, primary_key=True)
    id_user: int = Field(unique=True, foreign_key="user.id_user")
    documento_identificacion: int = Field(unique=True, foreign_key="documento_identificativo.id_documento")
    especialidad: int = Field(unique=True, foreign_key="especialidades.id_especialidad")
    matricula: str = Field(max_length=200, unique=True)
    create_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)

#porque se repiten columnas?? lo determinamos asi?
class Pacientes(SQLModel, table=True):
    __tablename__ = "pacientes"

    id_pacientes: Optional[int] = Field(default=None, primary_key=True)
    id_user: int = Field(unique=True, foreign_key="users.id_user")
    documento_identificacion: int = Field(unique=True, foreign_key="documento_identificativo.id_documento")
    especialidad: int = Field(unique=True, foreign_key="especialidades.id_especialidad")
    matricula: str = Field(max_length=200, unique=True)
    create_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)

class Turnos(SQLModel, table=True):
    __tablename__ = "turnos"
    
    id_turno: Optional[int] = Field(default=None, primary_key=True)
    id_medico: int = Field(foreign_key="medicos.id_medico")
    id_paciente: int = Field(foreign_key="pacientes.id_paciente")
    hora_entrada: datetime = Field()
    hora_salida: datetime = Field()
    completado_exitosamente: bool = Field()
    created_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)

class Consultas(SQLModel, table=True):
    __tablename__ = "consultas"
    
    id_consulta: Optional[int] = Field(default=None, primary_key=True)
    id_turno: int = Field(unique=True, foreign_key="turnos.id_turno")
    diagnostico: Optional[str] = Field(default=None)
    descripcion: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)

class Reviews(SQLModel, table=True):
    __tablename__ = "reviews"
    
    id_review: int = Field(primary_key=True)
    id_medico: int = Field(foreign_key="medicos.id_medico")
    id_paciente: int = Field(foreign_key="pacientes.id_paciente")
    calificacion: int = Field()
    comentario: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)