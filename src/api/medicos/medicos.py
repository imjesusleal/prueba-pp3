from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_db
from services.auth_services.jwt_service import jwt_service
from services.medicos.commands.get_all.get_all_cmd_handler import GetAllMedicosCmdHandler
from services.medicos.commands.get_all.get_medicos_cmd import GetAllMedicosCmd
from services.medicos.models.get_all_medicos_dto import GetAllMedicosDto

class MedicosRouter:
    def __init__(self):
        self.__get_all_handler = GetAllMedicosCmdHandler()
        
        self.router = APIRouter(prefix="/medicos", tags=["medicos"])
        self.router.get("/getAll", response_model=list[GetAllMedicosDto], status_code=200)(self.get_all)


    async def get_all(self,cmd: GetAllMedicosCmd = Depends(), db: AsyncSession = Depends(get_db), current_user: dict = Depends(jwt_service.get_current_user)) -> list[GetAllMedicosDto]:
        return await self.__get_all_handler.handle(cmd, db)
    
    
router = MedicosRouter()