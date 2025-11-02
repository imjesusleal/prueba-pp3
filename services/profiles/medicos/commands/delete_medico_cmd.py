from pydantic import BaseModel


class DeleteMedicoCmd(BaseModel):
    id_user: int