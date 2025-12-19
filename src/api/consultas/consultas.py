from fastapi import APIRouter, Depends

from db.db import get_db
from db.entities.users import Users
from services.auth_services.jwt_service import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession

from services.consultas.commands.create.create_consulta_cmd import CreateConsultasCmd
from services.consultas.commands.create.create_consulta_handler import CreateConsultaHandler
from services.consultas.commands.get_consulta_final.get_consulta_final_cmd import GetConsultaFinalCmd
from services.consultas.commands.get_consulta_final.get_consulta_final_handler import GetConsultaFinalHandler
from services.consultas.models.consultas_model import ConsultasModel




class ConsultasRouter():
    def __init__(self):
        self.router = APIRouter(prefix="/consultas", tags=["consultas"])
        self.router.post('/create', status_code=201)(self.create)
        self.router.get('/getConsultaFinal', response_model=ConsultasModel, status_code=200)(self.get_consulta_final)
        
    async def create(self, cmd: CreateConsultasCmd, db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
        handler = CreateConsultaHandler(db)
        await handler.handle(cmd)
        
    async def get_consulta_final(self, cmd: GetConsultaFinalCmd = Depends(), db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
        handler = GetConsultaFinalHandler(db)
        return await handler.handle(cmd)
        
router = ConsultasRouter()