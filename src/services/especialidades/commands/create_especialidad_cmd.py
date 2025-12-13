from pydantic import BaseModel


class CreateEspecialidadCmd(BaseModel):
    sigla_especialidad: str
    descripcion: str