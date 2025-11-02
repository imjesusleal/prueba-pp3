from pydantic import BaseModel


class MedicoProfile(BaseModel):
    id_medico: int
    id_user: int
    documento_identificativo: int
    especialidad: int
    matricula: str
    telefono: str
    nombre: str
    apellido: str
