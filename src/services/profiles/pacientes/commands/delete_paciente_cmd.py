from pydantic import BaseModel


class DeletePacienteCmd(BaseModel):
    id_user: int