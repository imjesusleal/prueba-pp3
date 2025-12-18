from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_db
from db.entities.users import Users
from services.auth_services.jwt_service import get_current_user
from services.medicos.commands.get_all.get_all_cmd_handler import GetAllMedicosCmdHandler
from services.medicos.commands.get_all.get_medicos_cmd import GetAllMedicosCmd
from services.medicos.commands.get_medico.get_medico_cmd import GetMedicoCmd
from services.medicos.commands.get_medico.get_medico_handler import GetMedicoHandler
from services.medicos.commands.get_turnos.get_turnos_handler import GetTurnosHandler
from services.medicos.models.get_all_medicos_dto import GetAllMedicosDto
from services.medicos.models.get_medico_dto import GetMedidoDto
from services.medicos.models.turnos_medico_dto import TurnosMedicosModel

class MedicosRouter:
    def __init__(self):
        
        self.router = APIRouter(prefix="/medicos", tags=["medicos"])
        self.router.get("/getAll", response_model=list[GetAllMedicosDto], status_code=200)(self.get_all)
        self.router.get("/get", response_model=GetMedidoDto, status_code=200)(self.get_medico)
        self.router.get("/getTurnos", response_model=list[TurnosMedicosModel], status_code = 200)(self.get_turnos)


    async def get_all(self,cmd: GetAllMedicosCmd = Depends(GetAllMedicosCmd), db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)) -> list[GetAllMedicosDto]:
        handler = GetAllMedicosCmdHandler(db)
        return await handler.handle(cmd)
    
    async def get_medico(self, cmd: GetMedicoCmd = Depends(), db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)) -> GetMedidoDto:
        handler = GetMedicoHandler(db)
        return await handler.handle(cmd)
    
    async def get_turnos(self, cmd: GetMedicoCmd = Depends(GetMedicoCmd), db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)) -> list[TurnosMedicosModel]: 
        handler = GetTurnosHandler(db) 
        return await handler.handle(cmd)
    
    
router = MedicosRouter()