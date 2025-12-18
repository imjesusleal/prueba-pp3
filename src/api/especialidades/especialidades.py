from fastapi import APIRouter, Depends
from db.db import get_db
from db.entities.users import Users
from services.auth_services.jwt_service import get_current_user
from services.especialidades.commands.create_especialidad_cmd import CreateEspecialidadCmd
from services.especialidades.handlers.create_especialidad_handler import CreateEspecialidadHandler
from services.especialidades.handlers.get_all_handler import GetAllEspecialidadesHandler
from services.especialidades.models.especialidades_dto import EspecialidadesDto
from sqlalchemy.ext.asyncio import AsyncSession


class EspecialidadesRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/especialidades", tags=["especialidades"])
        self.router.get("/getAll", response_model=list[EspecialidadesDto], status_code=200)(self.get_all)
        self.router.post("/create", status_code=201)(self.create)
        
    async def get_all(self, db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)) -> list[EspecialidadesDto]:
        handler = GetAllEspecialidadesHandler(db)
        return await handler.handle()

    async def create(self, cmd: CreateEspecialidadCmd, db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
        handler = CreateEspecialidadHandler(db)
        await handler.handle(cmd)

router = EspecialidadesRouter()