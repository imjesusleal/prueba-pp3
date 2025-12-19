from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from db.entities.turnos import Turnos
from db.entities.estados_turnos import EstadosTurnos
from enums.turnos_opciones import TurnosOpcionesEnums
from errors.turnos.turno_bad_update import TurnoBadUpdateError
from errors.turnos.turno_not_found_error import TurnoNotFoundError
from services.turnos.commands.update.update_turno_cmd import UpdateTurnoCmd
from repository.turnos import TurnosRepo

class UpdateTurnoHandler():
    def __init__(self, db: AsyncSession):
        self._db = db
        self._repo = TurnosRepo(db)
        
    async def handle(self, cmd: UpdateTurnoCmd):
        data: Optional[Turnos] = await self._repo.get_turno(cmd.id_turno, True)
         
        if data is None:
            #Esto no debería pasar porque ya lo genere
            raise TurnoNotFoundError('El turno enviado no se ha encontrado.', 404)
        
        if data.t_estado is None:
            data.t_estado = EstadosTurnos.create()
        
        if data.t_estado.id_turnos_opciones != TurnosOpcionesEnums.Pe.value:
            erroMsg = ''
            match data.t_estado.id_turnos_opciones:
                case TurnosOpcionesEnums.Ca.value:
                    errorMsg = 'Cancelado'
                case TurnosOpcionesEnums.Co.value:
                    errorMsg = 'Completado'
            raise TurnoBadUpdateError(f'El turno a modificar debe estar en estado Pendiente. El turno enviado se encuentra en estado: {errorMsg}')
        
        data.t_estado.modificar_estado(cmd.nuevo_estado, cmd.clasificacion)
        
        await self._db.commit()