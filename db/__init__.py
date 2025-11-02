from .entities.consultas import Consulta
from .entities.documento_identificativo import DocumentoIdentificativo
from .entities.especialidades import Especialidades
from .entities.medicos import Medicos
from .entities.pacientes import Pacientes
from .entities.reviews import Reviews
from .entities.turnos import Turnos
from .entities.users_roles import UsersRoles
from .entities.users import Users
from .entities.refresh_token import RefreshToken

Users.model_rebuild()
Medicos.model_rebuild()
Pacientes.model_rebuild()

__all__ = ['get_db', 'Consulta']
