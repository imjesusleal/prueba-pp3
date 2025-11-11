from pydantic import BaseModel


class PacienteProfile(BaseModel):
    id_paciente: int
    id_user: int
    documento_identificativo: int
    nombre: str
    apellido: str
    img_name: str | None
