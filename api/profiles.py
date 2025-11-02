from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_db
from models.profiles.medifco_profile import MedicoProfile
from services.auth_services.jwt_service import jwt_service
from services.profiles.medicos.commands.add_medico_command import AddMedicoCommand
from services.profiles.medicos.commands.delete_medico_cmd import DeleteMedicoCmd
from services.profiles.medicos.handlers.medico_profile import MedicoProfileHandler


class ProfilesRouter:
    def __init__(self):
        self.__medico_handler = MedicoProfileHandler()

        self.router = APIRouter(prefix="/profiles", tags=["profiles"])
        self.router.get("/get", response_model=MedicoProfile, status_code=200)(self.get_profile)
        self.router.post("/create",status_code=201)(self.create_medico)
        self.router.post("/delete", status_code=202)(self.delete_medico)

    async def get_profile(self, user_id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(jwt_service.get_current_user)):
        return await self.__medico_handler.get_user_medico(user_id, db) 

    async def create_medico(self, cmd: AddMedicoCommand, db: AsyncSession = Depends(get_db), current_user: dict = Depends(jwt_service.get_current_user)):
        await self.__medico_handler.create_medico(cmd, db)

    async def delete_medico(self, cmd: DeleteMedicoCmd, db: AsyncSession = Depends(get_db), current_user: dict = Depends(jwt_service.get_current_user)):
        await self.__medico_handler.delete_medico(cmd, db)

router = ProfilesRouter()