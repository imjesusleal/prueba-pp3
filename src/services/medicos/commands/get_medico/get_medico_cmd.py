from pydantic import BaseModel


class GetMedicoCmd(BaseModel):
    id_medico: int