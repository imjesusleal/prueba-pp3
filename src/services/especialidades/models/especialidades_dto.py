from pydantic import BaseModel


class EspecialidadesDto(BaseModel):
    id_especialidad: int
    sigla_especialidad: str
    descripcion: str     