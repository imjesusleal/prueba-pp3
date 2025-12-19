from pydantic import BaseModel

from enums.turnos_opciones import TurnosOpcionesEnums


class UpdateTurnoCmd(BaseModel):
    id_turno: int
    nuevo_estado: TurnosOpcionesEnums
    clasificacion: int | None = None