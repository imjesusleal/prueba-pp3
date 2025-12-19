from sqlalchemy.ext.asyncio import AsyncSession

from errors.consultas.consulta_already_created import ConsultaAlreadyCreated
from repository.consultas import ConsultasRepo
from db.entities.consultas import Consulta
from services.consultas.commands.create.create_consulta_cmd import CreateConsultasCmd

class CreateConsultaHandler:
    def __init__(self, db: AsyncSession):
        self._db = db
        self._repo = ConsultasRepo(db)
        
    async def handle(self, cmd: CreateConsultasCmd):
        
        existeConsulta = await self._repo.existe(cmd.id_turno)
        
        if existeConsulta:
            raise ConsultaAlreadyCreated('La consulta del turno enviado ya ha sido creada. ', 400)
        
        consulta = Consulta.create(cmd.id_turno, cmd.diagnostico, cmd.descripcion)
        self._repo.add(consulta)
        await self._db.commit()
        