from fastapi import APIRouter, Depends

from db.db import get_db
from db.entities.users import Users
from services.auth_services.jwt_service import get_current_user
from services.turnos.commands.create.create_turno_cmd import CreateTurnoCmd
from sqlalchemy.ext.asyncio import AsyncSession

from services.turnos.commands.create.create_turno_handler import CreateCmdHandler
from services.turnos.commands.get_all.get_all_turnos_cmd import GetAllTurnosCmd
from services.turnos.commands.get_all.get_all_turnos_handler import GetAllTurnosHandler
from services.turnos.commands.get_all_atenciones_medicas.get_all_atenciones_medicas_cmd import GetAllAtencionesMedicasCmd
from services.turnos.commands.get_all_atenciones_medicas.get_all_atenciones_medicas_handler import GetAllAtencionesMedicasHandler
from services.turnos.commands.get_all_proximos_turnos.get_all_proximos_turnos_cmd import GetAllProximosTurnosCmd
from services.turnos.commands.get_all_proximos_turnos.get_all_proximos_turnos_handler import GetAllProximosTurnosHandler
from services.turnos.commands.update.update_turno_cmd import UpdateTurnoCmd
from services.turnos.commands.update.update_turno_handler import UpdateTurnoHandler
from services.turnos.models.historial_atenciones import HistorialAtencionesModel
from services.turnos.models.historial_paciente import HistorialPacienteModel

class TurnosRouter():
    def __init__(self):
        
        self.router = APIRouter(prefix="/turnos", tags=["turnos"])
        self.router.post("/create", status_code=201)(self.create)
        self.router.post("/update", status_code=201)(self.update)
        self.router.get("/getAll", response_model=list[HistorialPacienteModel] ,status_code=200)(self.get_all)
        self.router.get("/getAllProximosTurnos", response_model=list[HistorialPacienteModel], status_code=200)(self.get_all_proximos_turnos)
        self.router.get("/getAllAtencionesMedico", response_model=list[HistorialAtencionesModel], status_code=200)(self.get_all_atenciones_medico)
        
    async def create(self, cmd: CreateTurnoCmd, db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
        handler = CreateCmdHandler(db)
        await handler.handle(cmd)
        
    async def update(self, cmd: UpdateTurnoCmd, db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)): 
        handler = UpdateTurnoHandler(db)
        await handler.handle(cmd)
    
    async def get_all(self, cmd: GetAllTurnosCmd = Depends(), db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
        handler = GetAllTurnosHandler(db)
        return await handler.handle(cmd)
    
    async def get_all_proximos_turnos(self, cmd: GetAllProximosTurnosCmd = Depends(), db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
        handler = GetAllProximosTurnosHandler(db)
        return await handler.handle(cmd)
    
    async def get_all_atenciones_medico(self, cmd: GetAllAtencionesMedicasCmd = Depends(), db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
        handler = GetAllAtencionesMedicasHandler(db)
        return await handler.handle(cmd)
      
router = TurnosRouter()