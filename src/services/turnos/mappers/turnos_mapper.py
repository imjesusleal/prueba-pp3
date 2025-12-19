from datetime import datetime

from enums.turnos_opciones import TurnosOpcionesEnums
from services.turnos.models.historial_atenciones import HistorialAtencionesModel
from services.turnos.models.historial_paciente import HistorialPacienteModel


class MapperTurnos:
    
    
    @staticmethod
    def map_to_historial_pacientes(id_turno: int, 
                                   nombre_medico: str, 
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
            id_turno = id_turno,
            nombre_medico=nombre_medico,
            apellido_medico=apellido_medico,
            especialidad=especialidad,
            fecha_turno=fecha_turno,
            clasificacion=clasificacion if clasificacion is not None else 0,
            observaciones=observaciones,
            estado_turno = estado_res
        )
        
        
    @staticmethod
    def map_to_historial_atenciones(id_turno:int,
                                    id_medico: int,
                                    id_paciente: int,
                                    nombre_paciente: str,
                                    apellido_paciente: str,
                                    hora_atencion: datetime,
                                    estado: TurnosOpcionesEnums,
                                    especialidad: str
                                    ) -> HistorialAtencionesModel:
        
        estado_res = ''
        
        match estado:
            case TurnosOpcionesEnums.Pe:
                estado_res = 'Pendiente'
            case TurnosOpcionesEnums.Co:
                estado_res = 'Completado'
            case TurnosOpcionesEnums.Ca:
                estado_res = 'Cancelado'
                
        return HistorialAtencionesModel(
            id_turno = id_turno,
            id_medico=id_medico,
            id_paciente=id_paciente,
            nombre_paciente=nombre_paciente,
            apellido_paciente=apellido_paciente,
            hora_atencion=hora_atencion,
            especialidad=especialidad,
            estado=estado_res
        )