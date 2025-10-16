from fastapi import Depends
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import db, get_db
from models.medify_models import (
    UserRoles, Users, Especialidades, DocumentoIdentificativo,
    Medicos, Pacientes, Turnos, Consultas, Reviews)
from typing import List, Optional

"""
Funciones asyn,
CRUD,
Consultas por campos únicos
"""
# ======================== USERS ROLES REPOSITORY ========================
async def get_all_users_roles(db: AsyncSession) -> List[UserRoles]:
    res = await db.execute(select(UserRoles))
    #es equivalente a escribir en SQL: SELECT * FROM users_roles/db.execute se consulta a la BD y se espera la respuesta en el 'res'
    return res.scalars().all()#lo devuelve en una lista

async def get_user_role(id: int, db: AsyncSession) -> Optional[UserRoles]:
    query = select(UserRoles).filter(UserRoles.id_users_roles == id)#se puede traducir como un WHERE
    res = await db.execute(query)
    return res.scalars().first()

async def get_user_role_by_rol(rol: str, db: AsyncSession) -> Optional[UserRoles]:
    query = select(UserRoles).filter(UserRoles.rol == rol)#funciona como un WHERE rol 
    res = await db.execute(query)
    return res.scalars().first()

# ======================== USERS REPOSITORY ========================
async def get_all_user(db: AsyncSession) -> List[Users]:#trae todos los usuarios
    res = await db.execute(select(Users))
    return res.scalars().all()

async def get_user(id: int, db: AsyncSession) -> Optional[Users]:#trae a los usuarios por su id
    query = select(Users).filter(Users.id_user == id)
    res = await db.execute(query)
    return res.scalars().first()

async def get_user_by_username(username: str, db: AsyncSession) -> Optional[Users]:#busca usuarios por su username
    query = select(Users).filter(Users.username == username)
    res = await db.execute(query)
    return res.scalars().first()

async def get_user_by_email(email: str, db: AsyncSession) -> Optional[Users]:#busca usuarios por su mail
    query = select(Users).filter(Users.email == email)
    res = await db.execute(query)
    return res.scalars().first()

# ======================== ESPECIALIDADES REPOSITORY ========================
async def get_all_especialidades(db:AsyncSession)-> List[Especialidades]:
    res = await db.execute(select(Especialidades))
    return res.scalars().all()

async def get_especialidad(id:int, db:AsyncSession)-> Optional[Especialidades]:
    query = select(Especialidades).filter(Especialidades.sigla_especialidad == id)
    res = await db.execute(query)
    return res.scalars().first()

async def get_especialidad_by_sigla(sigla:str, db:AsyncSession)-> Optional[Especialidades]:
    query = select(Especialidades).filter(Especialidades.sigla_especialidad == sigla)
    res = await db.execute(query)
    return res.scalars().first()

# ======================== DOCUMENTO IDENTIFICATIVO REPOSITORY ========================
async def get_all_documentos(db: AsyncSession) -> List[DocumentoIdentificativo]:
    res = await db.execute(select(DocumentoIdentificativo))
    return res.scalars().all()

async def get_documento(id: int, db: AsyncSession) -> Optional[DocumentoIdentificativo]:
    query = select(DocumentoIdentificativo).filter(DocumentoIdentificativo.id_documento == id)
    res = await db.execute(query)
    return res.scalars().first()

async def get_documento_by_tipo(tipo: str, db: AsyncSession) -> Optional[DocumentoIdentificativo]:
    query = select(DocumentoIdentificativo).filter(DocumentoIdentificativo.tipo_documento == tipo)
    res = await db.execute(query)
    return res.scalars().first()

# ======================== MEDICOS REPOSITORY ========================
async def get_all_medicos(db: AsyncSession) -> List[Medicos]:
    res = await db.execute(select(Medicos))
    return res.scalars().all()

async def get_medico(id: int, db: AsyncSession) -> Optional[Medicos]:
    query = select(Medicos).filter(Medicos.id_medico == id)
    res = await db.execute(query)
    return res.scalars().first()

async def get_medico_by_user(id_user: int, db: AsyncSession) -> Optional[Medicos]:#conecta un perfil usuario con un perfil medico
    query = select(Medicos).filter(Medicos.id_user == id_user)
    res = await db.execute(query)
    return res.scalars().first()

async def get_medico_by_matricula(matricula: str, db: AsyncSession) -> Optional[Medicos]:#busca un medico por su matricula
    query = select(Medicos).filter(Medicos.matricula == matricula)
    res = await db.execute(query)
    return res.scalars().first()

async def get_medicos_by_especialidad(especialidad_id: int, db: AsyncSession) -> List[Medicos]:#busca por especialidad
    query = select(Medicos).filter(Medicos.especialidad == especialidad_id)
    res = await db.execute(query)
    return res.scalars().all()

# ======================== PACIENTES REPOSITORY ========================
async def get_all_pacientes(db: AsyncSession) -> List[Pacientes]:
    res = await db.execute(select(Pacientes))
    return res.scalars().all()

async def get_paciente(id: int, db: AsyncSession) -> Optional[Pacientes]:
    query = select(Pacientes).filter(Pacientes.id_pacientes == id)
    res = await db.execute(query)
    return res.scalars().first()

async def get_paciente_by_user(id_user: int, db: AsyncSession) -> Optional[Pacientes]:
    query = select(Pacientes).filter(Pacientes.id_user == id_user)
    res = await db.execute(query)
    return res.scalars().first()

async def get_paciente_by_matricula(matricula: str, db: AsyncSession) -> Optional[Pacientes]:
    query = select(Pacientes).filter(Pacientes.matricula == matricula)
    res = await db.execute(query)
    return res.scalars().first()

# ======================== TURNOS REPOSITORY ========================
async def get_all_turnos(db: AsyncSession) -> List[Turnos]:#Es necesario que llame primero a todos los turnos
    res = await db.execute(select(Turnos))
    return res.scalars().all()

async def get_turno(id: int, db: AsyncSession) -> Optional[Turnos]:
    query = select(Turnos).filter(Turnos.id_turno == id)
    res = await db.execute(query)
    return res.scalars().first()

async def get_turnos_by_medico(id_medico: int, db: AsyncSession) -> List[Turnos]:
    query = select(Turnos).filter(Turnos.id_medico == id_medico)
    res = await db.execute(query)
    return res.scalars().all()

async def get_turnos_by_paciente(id_paciente: int, db: AsyncSession) -> List[Turnos]:#bsuqueda por turnos que hace el paciente
    query = select(Turnos).filter(Turnos.id_paciente == id_paciente)
    res = await db.execute(query)
    return res.scalars().all()

async def get_turnos_completados(db: AsyncSession) -> List[Turnos]:#turno ya completados, filtro
    query = select(Turnos).filter(Turnos.completado_exitosamente == True)
    res = await db.execute(query)
    return res.scalars().all()

async def get_turnos_pendientes(db: AsyncSession) -> List[Turnos]:
    query = select(Turnos).filter(Turnos.completado_exitosamente == False)
    res = await db.execute(query)
    return res.scalars().all()

# ======================== CONSULTAS REPOSITORY ========================
async def get_all_consultas(db: AsyncSession) -> List[Consultas]:
    res = await db.execute(select(Consultas))
    return res.scalars().all()

async def get_consulta(id: int, db: AsyncSession) -> Optional[Consultas]:
    query = select(Consultas).filter(Consultas.id_consulta == id)
    res = await db.execute(query)
    return res.scalars().first()

async def get_consulta_by_turno(id_turno: int, db: AsyncSession) -> Optional[Consultas]:
    query = select(Consultas).filter(Consultas.id_turno == id_turno)
    res = await db.execute(query)
    return res.scalars().first()

# ======================== REVIEWS REPOSITORY ========================
async def get_all_reviews(db: AsyncSession) -> List[Reviews]:
    res = await db.execute(select(Reviews))
    return res.scalars().all()

async def get_review(id: int, db: AsyncSession) -> Optional[Reviews]:
    query = select(Reviews).filter(Reviews.id_review == id)
    res = await db.execute(query)
    return res.scalars().first()

async def get_reviews_by_medico(id_medico: int, db: AsyncSession) -> List[Reviews]:
    query = select(Reviews).filter(Reviews.id_medico == id_medico)
    res = await db.execute(query)
    return res.scalars().all()

async def get_reviews_by_paciente(id_paciente: int, db: AsyncSession) -> List[Reviews]:
    query = select(Reviews).filter(Reviews.id_paciente == id_paciente)
    res = await db.execute(query)
    return res.scalars().all()

async def get_reviews_by_calificacion(calificacion: int, db: AsyncSession) -> List[Reviews]:
    query = select(Reviews).filter(Reviews.calificacion == calificacion)
    res = await db.execute(query)
    return res.scalars().all()