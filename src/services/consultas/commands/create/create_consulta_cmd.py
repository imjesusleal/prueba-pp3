from pydantic import BaseModel


class CreateConsultasCmd(BaseModel):
    id_turno: int
    diagnostico: str | None = None
    descripcion: str | None = None