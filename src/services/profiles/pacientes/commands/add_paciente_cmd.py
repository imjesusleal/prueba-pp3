from pydantic import BaseModel


class AddPacienteCmd(BaseModel): 
    id_user: int
    documento_identificativo: int
    nombre: str
    apellido: str
