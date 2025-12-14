from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_db
from errors.json_token.wrong_json_token import WrongJsonToken
from models.profiles.paciente_profile import PacienteProfile
from services.auth_services.jwt_service import get_current_user
from services.profiles.pacientes.commands.add_paciente_cmd import AddPacienteCmd
from services.profiles.pacientes.commands.delete_paciente_cmd import DeletePacienteCmd
from services.profiles.pacientes.commands.updt_paciente_cmd import UpdtPacienteCommand
from services.profiles.pacientes.handlers.paciente_profile import PacienteProfileHandler


class PacientesProfileRouter:
    def __init__(self):

        self.router = APIRouter(prefix="/profiles/pacientes", tags=["profiles/pacientes"])
        self.router.get("/get", response_model=PacienteProfile, status_code=200)(self.get_profile)
        self.router.post("/create",status_code=201)(self.create_paciente)
        self.router.post("/update",status_code=201)(self.update_paciente)
        self.router.post("/delete", status_code=202)(self.delete_paciente)

    async def get_profile(self, user_id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
        handler = PacienteProfileHandler(db)
        return await handler.get_user_paciente(user_id) 

    async def create_paciente(self, cmd: AddPacienteCmd, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
        handler = PacienteProfileHandler(db)
        await handler.create_paciente(cmd)

    async def update_paciente(self, cmd: UpdtPacienteCommand, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):

        if not current_user["id_user"]:
            raise WrongJsonToken("El token enviado no posee las especificaciones técnicas correctas. ", 400)

        handler = PacienteProfileHandler(db)
        await handler.update_perfil_paciente(current_user["id_user"], cmd)

    async def delete_paciente(self, cmd: DeletePacienteCmd, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
        handler = PacienteProfileHandler(db)
        await handler.delete_paciente(cmd)

router = PacientesProfileRouter()