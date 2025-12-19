from pydantic import BaseModel


class GetAllProximosTurnosCmd(BaseModel):
    id_paciente: int