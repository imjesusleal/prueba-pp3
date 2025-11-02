from pydantic import BaseModel


class MedicoProfile(BaseModel):
    id_medico: int
    id_user: int
    documento_identificativo: int
    especialidad: int
    matricula: str
    telefono: str | None
    nombre: str
    apellido: str
    img_bytes: str | None
