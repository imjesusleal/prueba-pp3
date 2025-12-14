from fastapi import Depends
from db.db import get_db
from db.entities.users import Users
from errors.medicos.wront_rol_error import WrongRolError
from errors.pacientes.medico_already_created import PacienteAlreadyCreated
from errors.pacientes.paciente_not_found import PacienteNotFound
from errors.users.user_not_found_error import UserNotFoundError
from models.profiles.medifco_profile import MedicoProfile
from repository.pacientes import PacienteRepo
from repository.users import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from services.profiles.enums.profiles_enums import ProfilesEnum
from services.profiles.pacientes.commands.add_paciente_cmd import AddPacienteCmd
from services.profiles.pacientes.commands.delete_paciente_cmd import DeletePacienteCmd
from services.profiles.pacientes.commands.updt_paciente_cmd import UpdtPacienteCommand

class PacienteProfileHandler:
    def __init__(self, db: AsyncSession):
        self.__user_repo = UserRepository(db)
        self.__paciente_repo = PacienteRepo(db)
        self._db = db

    async def get_user_paciente(self, id_user:int) -> MedicoProfile: 
        user: Users = await self.__user_repo.get_user_with_paciente_profile(id_user)

        if user is None:
            raise UserNotFoundError("El usuario no ha sido encontrado", 404)
        
        if user.paciente == None:
            raise PacienteNotFound("El usuario enviado no posee un perfil de paciente generado. ", 404)
        
        return user.paciente.map_to_model()

    async def create_paciente(self, cmd: AddPacienteCmd): 

        user: Users = await self.__user_repo.get_user_with_paciente_profile(cmd.id_user)

        if user is None:
            raise UserNotFoundError("El usuario no ha sido encontrado", 404)

        if user.user_rol != ProfilesEnum.P.value:
            raise WrongRolError("El rol del usuario creado no corresponde con el pérfil de pacientes. Por favor, modifique su usuario si desea generar un perfil de paciente.", 400)

        if user.paciente != None:
            raise PacienteAlreadyCreated("El usuario enviado ya posee un perfil de médico generado", 400)
    
        
        user.create_paciente(cmd)

        await self._db.commit()

    async def update_perfil_paciente(self,user_id:int, cmd: UpdtPacienteCommand):
        user: Users = await self.__user_repo.get_user_with_paciente_profile(user_id)

        if user is None:
            raise UserNotFoundError("El usuario no ha sido encontrado", 404)

        if user.user_rol != ProfilesEnum.P.value:
            raise WrongRolError("El rol del usuario creado no corresponde con el pérfil de paciente. Por favor, modifique su usuario si desea generar un perfil de paciente.", 400)

        if user.paciente == None:
            raise PacienteAlreadyCreated("El usuario enviado no posee un perfil de médico generado", 400)
        
        user.paciente.update_self(cmd)

        await self._db.commit()
    

    async def delete_paciente(self, cmd: DeletePacienteCmd): 
        user: Users = await self.__user_repo.get_user_with_paciente_profile(cmd.id_user)

        if user is None:
            raise UserNotFoundError("El usuario no ha sido encontrado", 404)

        if user.user_rol != ProfilesEnum.P.value:
            raise WrongRolError("El rol del usuario creado no corresponde con el pérfil de médicos. No puede darse de baja al perfil. ", 400)

        if user.medico == None:
            raise PacienteAlreadyCreated("El usuario enviado no posee un perfil de médico generado. ", 400)
    
        
        await self.__paciente_repo.delete_paciente(user.paciente)
        user.delete_paciente()

        await self._db.commit()