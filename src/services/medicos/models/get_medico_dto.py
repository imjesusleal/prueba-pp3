from pydantic import BaseModel


class GetMedidoDto(BaseModel):
    id_medico: int
    nombre: str
    apellido: str
    matricula: str
    especialidad: str
    rating: float
    reviews: int
    atenciones: int
    turnos_pendientes: int
    img_name: str | None
    