from fastapi import Depends
from db.db import get_db
from db.entities.users import Users
from errors.medicos.medico_already_created import MedicoAlreadyCreated
from errors.medicos.medico_not_found import MedicoNotFound
from errors.medicos.wront_rol_error import WrongRolError
from errors.users.user_not_found_error import UserNotFoundError
from models.profiles.medifco_profile import MedicoProfile
from repository.medicos import MedicosRepo
from repository.users import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession

from services.profiles.enums.profiles_enums import ProfilesEnum
from services.profiles.medicos.commands.add_medico_command import AddMedicoCommand
from services.profiles.medicos.commands.delete_medico_cmd import DeleteMedicoCmd


class MedicoProfileHandler:
    def __init__(self):
        self.__user_repo = UserRepository()
        self.__medico_repo = MedicosRepo()

    async def get_user_medico(self, id_user:int, db: AsyncSession = Depends(get_db)) -> MedicoProfile: 
        user: Users = await self.__user_repo.get_user_with_medico_profile(id_user, db)

        if user is None:
            raise UserNotFoundError("El usuario no ha sido encontrado", 404)
        
        if user.medico == None:
            raise MedicoNotFound("El usuario enviado no posee un perfil de médico generado. ", 404)
        
        return user.medico.map_to_model()

    async def create_medico(self, cmd: AddMedicoCommand, db: AsyncSession = Depends(get_db)): 
        user: Users = await self.__user_repo.get_user_with_medico_profile(cmd.id_user, db)

        if user is None:
            raise UserNotFoundError("El usuario no ha sido encontrado", 404)

        if user.user_rol != ProfilesEnum.M.value:
            raise WrongRolError("El rol del usuario creado no corresponde con el pérfil de médicos. Por favor, modifique su usario si desea generar un perfil de médico.", 400)

        if user.medico != None:
            raise MedicoAlreadyCreated("El usuario enviado ya posee un perfil de médico generado", 400)
    
        
        user.create_medico(cmd)

        await db.commit()

    async def delete_medico(self, cmd: DeleteMedicoCmd, db: AsyncSession = Depends(get_db)): 
        user: Users = await self.__user_repo.get_user_with_medico_profile(cmd.id_user, db)

        if user is None:
            raise UserNotFoundError("El usuario no ha sido encontrado", 404)

        if user.user_rol != ProfilesEnum.M.value:
            raise WrongRolError("El rol del usuario creado no corresponde con el pérfil de médicos. No puede darse de baja al perfil. ", 400)

        if user.medico == None:
            raise MedicoAlreadyCreated("El usuario enviado no posee un perfil de médico generado. ", 400)
    
        
        await self.__medico_repo.delete_medico(user.medico, db)
        user.delete_medico()

        await db.commit()
        
        
        