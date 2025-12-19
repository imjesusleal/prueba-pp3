from pydantic import BaseModel


class GetConsultaFinalCmd(BaseModel):
    id_turno: int