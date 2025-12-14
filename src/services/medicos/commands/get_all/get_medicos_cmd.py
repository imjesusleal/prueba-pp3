from pydantic import BaseModel
from typing import Optional


class GetAllMedicosCmd(BaseModel):
    especialidad: Optional[int] = None
    clasificacion: int
    cursor_id: int 
    limit: int
    