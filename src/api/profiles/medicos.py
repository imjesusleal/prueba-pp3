from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_db
from db.entities.users import Users
from errors.json_token.wrong_json_token import WrongJsonToken
from models.profiles.medifco_profile import MedicoProfile
from services.auth_services.jwt_service import get_current_user
from services.profiles.medicos.commands.add_medico_command import AddMedicoCommand
from services.profiles.medicos.commands.delete_medico_cmd import DeleteMedicoCmd
from services.profiles.medicos.commands.updt_medico_command import UpdtMedicoCommand
from services.profiles.medicos.handlers.medico_profile import MedicoProfileHandler


class MedicosProfileRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/profiles/medicos", tags=["profiles/medicos"])
        self.router.get("/get", response_model=MedicoProfile, status_code=200)(self.get_profile)
        self.router.post("/create",status_code=201)(self.create_medico)
        self.router.post("/update",status_code=201)(self.update_medico)
        self.router.post("/delete", status_code=202)(self.delete_medico)

    async def get_profile(self, user_id: int, db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
        handler = MedicoProfileHandler(db)
        return await handler.get_user_medico(user_id) 

    async def create_medico(self, cmd: AddMedicoCommand, db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
        handler = MedicoProfileHandler(db)
        await handler.create_medico(cmd)

    async def update_medico(self, cmd: UpdtMedicoCommand, db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):

        if not current_user.id_user:
            raise WrongJsonToken("El token enviado no posee las especificaciones técnicas correctas. ", 400)

        handler = MedicoProfileHandler(db)
        await handler.update_perfil_medico(current_user.id_user, cmd)

    async def delete_medico(self, cmd: DeleteMedicoCmd, db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
        handler = MedicoProfileHandler(db)
        await handler.delete_medico(cmd)

router = MedicosProfileRouter()