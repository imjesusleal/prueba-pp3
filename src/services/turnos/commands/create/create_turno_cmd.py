from datetime import datetime
from pydantic import BaseModel

from errors.turnos.mal_horario_enviado_error import MalHorarioEnviadoError


class CreateTurnoCmd(BaseModel):
    id_medico: int
    id_paciente: int
    hora_entrada: datetime
    hora_salida: datetime
    
    
    def validar(self) -> None:
        if (self.hora_entrada > self.hora_salida):
            raise MalHorarioEnviadoError("La hora de entrada no puede ser mayor a la hora de salida. ", 400)
        
        if (self.hora_entrada < datetime.now()):
            raise MalHorarioEnviadoError("La hora de entrada no puede ser menor a la hora actual. ", 400)
        
        hourDif = self.hora_entrada.hour - self.hora_salida.hour
        
        if abs(hourDif) > 2:
            raise MalHorarioEnviadoError("El horario de las consultas es como máximo de dos horas. ")
        
        
        