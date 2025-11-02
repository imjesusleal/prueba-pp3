from pydantic import BaseModel


class UpdtMedicoCommand(BaseModel): 
    matricula: str
    telefono: str