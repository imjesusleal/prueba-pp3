from datetime import datetime

from enums.turnos_opciones import TurnosOpcionesEnums
from services.turnos.models.historial_paciente import HistorialPacienteModel


class MapperTurnos:
    
    
    @staticmethod
    def map_to_historial_pacientes(nombre_medico: str, 
                                   apellido_medico: str, 
                                   especialidad: str, 
                                   fecha_turno: datetime, 
                                   clasificacion: int, 
                                   observaciones: str, 
                                   estado: TurnosOpcionesEnums) -> HistorialPacienteModel:
        
        estado_res = ''
        
        match estado:
            case TurnosOpcionesEnums.Pe:
                estado_res = 'Pendiente'
            case TurnosOpcionesEnums.Co:
                estado_res = 'Completado'
            case TurnosOpcionesEnums.Ca:
                estado_res = 'Cancelado'
        
        return HistorialPacienteModel(
            nombre_medico=nombre_medico,
            apellido_medico=apellido_medico,
            especialidad=especialidad,
            fecha_turno=fecha_turno,
            clasificacion=clasificacion if clasificacion is not None else 0,
            observaciones=observaciones,
            estado_turno = estado_res
        )