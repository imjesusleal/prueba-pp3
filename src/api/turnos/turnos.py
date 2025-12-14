from fastapi import APIRouter, Depends

from db.db import get_db
from services.auth_services.jwt_service import get_current_user
from services.turnos.commands.create.create_turno_cmd import CreateTurnoCmd
from sqlalchemy.ext.asyncio import AsyncSession

from services.turnos.commands.create.create_turno_handler import CreateCmdHandler

class TurnosRouter():
    def __init__(self):
        
        self.router = APIRouter(prefix="/turnos", tags=["turnos"])
        self.router.post("/create", status_code=201)(self.create)
        
    async def create(self, cmd: CreateTurnoCmd, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
        handler = CreateCmdHandler(db)
        await handler.handle(cmd)
        
router = TurnosRouter()