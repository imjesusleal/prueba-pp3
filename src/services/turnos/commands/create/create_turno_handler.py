from fastapi import Depends
from db.db import get_db
from db.entities.turnos import Turnos
from errors.turnos.turno_ocupado_error import TurnoOcupadoError
from services.turnos.commands.create.create_turno_cmd import CreateTurnoCmd
from repository.turnos import TurnosRepo
from sqlalchemy.ext.asyncio import AsyncSession


class CreateCmdHandler():
    def __init__(self, db: AsyncSession):
        self._repo = TurnosRepo(db)
        self._db = db
        
    async def handle(self, cmd: CreateTurnoCmd):
        
        cmd.validar()
        
        existe_turno = await self._repo.get_turno_between_fecha(cmd.hora_entrada, cmd.hora_salida,True)
        
        if existe_turno is not None: 
            hora_entrada = cmd.hora_entrada.time()
            hora_salida = cmd.hora_salida.time()
            raise TurnoOcupadoError(f"El turno enviado entre le horario {hora_entrada} y {hora_salida}", 400)
        
        turno = Turnos.create(cmd.id_medico, cmd.id_paciente, cmd.hora_entrada, cmd.hora_salida)
        
        print(id(self._repo._db))
        print(id(self._db))
        
        self._repo.add(turno)
        await self._db.commit()
        await self._db.refresh(turno)
        
        if not turno.id_turno:
            raise Exception("No se que paso")
        
        
        
        