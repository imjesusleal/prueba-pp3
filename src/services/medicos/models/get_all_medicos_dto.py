
from pydantic import BaseModel


class GetAllMedicosDto(BaseModel):
    id_medico: int
    nombre: str
    apellido: str
    matricula: str
    especialidad: str
    rating: float
    reviews: int
    img_name: str | None
    
    