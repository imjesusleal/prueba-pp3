from db.entities.medicos import Medicos
from services.medicos.models.get_all_medicos_dto import GetAllMedicosDto
from services.medicos.models.get_medico_dto import GetMedidoDto

class MedicosMapper:
    
    @staticmethod
    def map_to_grid_model(medico_entity: Medicos, rating: float, reviews: int) -> GetAllMedicosDto:
        return GetAllMedicosDto(
            id_medico=medico_entity.id_medico,
            nombre=medico_entity.nombre,
            apellido=medico_entity.apellido,
            matricula=medico_entity.matricula,
            rating= rating,
            reviews=reviews,
            especialidad=medico_entity.m_especialidad.descripcion,
            img_name=medico_entity.img_name
        )
        
    @staticmethod 
    def map_to_dto(medico_entity: Medicos, rating: float, reviews: int, atenciones: int, turnos_pendientes: int):
        return GetMedidoDto(
            id_medico=medico_entity.id_medico,
            nombre=medico_entity.nombre,
            apellido=medico_entity.apellido,
            matricula=medico_entity.matricula,
            rating= rating,
            reviews=reviews,
            atenciones = atenciones, 
            turnos_pendientes=turnos_pendientes,
            especialidad=medico_entity.m_especialidad.descripcion,
            img_name=medico_entity.img_name
        )