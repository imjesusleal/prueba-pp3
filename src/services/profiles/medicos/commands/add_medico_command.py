from pydantic import BaseModel


class AddMedicoCommand(BaseModel): 
    id_user: int
    documento_identificativo: int
    especialidad: int
    matricula: str
    telefono: str
    nombre: str
    apellido: str
