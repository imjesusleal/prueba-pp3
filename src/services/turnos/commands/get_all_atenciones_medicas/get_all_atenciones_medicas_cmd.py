from pydantic import BaseModel


class GetAllAtencionesMedicasCmd(BaseModel):
    id_medico: int
    estado: int | None = None