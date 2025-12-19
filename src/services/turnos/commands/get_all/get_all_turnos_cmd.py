from pydantic import BaseModel


class GetAllTurnosCmd(BaseModel):
    id_paciente: int