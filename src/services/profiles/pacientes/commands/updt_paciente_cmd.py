from pydantic import BaseModel


class UpdtPacienteCommand(BaseModel): 
    nombre: str
    apellido: str