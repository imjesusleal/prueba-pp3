from datetime import datetime
from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from db.entities.refresh_token import RefreshToken
from errors.admin.cant_register_admin_error import CantRegisterAdminError
from errors.ierror_interface import IError
from errors.refresh_token.refresh_token_invalid_error import RefreshTokenInvalidError
from errors.users.email_used_error import EmailUsedError
from errors.users.rol_not_found_error import RolNotFoundError
from errors.users.user_created_error import UserCreatedError
from models.auth_models.refresh_model import RefreshModel
from models.auth_models.token_response import UserResponse
from models.auth_models.user_login import UserLogin
from models.auth_models.user_register import UserRegister
from repository.refresh_token import RefreshTokenRepo
from repository.user_roles import UsersRolesRepository
from repository.users import UserRepository
from db.entities.users import Users
from db.db import get_db
from services.auth_services.jwt_service import JwtService
from services.profiles.enums.profiles_enums import ProfilesEnum

class AuthServices: 

    def __init__(self):
        self.__roles_repository = UsersRolesRepository()
        self.__user_repository = UserRepository()
        self.__refresh_token_repo: RefreshTokenRepo = RefreshTokenRepo()
        self.__jwt_service: JwtService = JwtService()

    __pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    async def register_user(self, user_data: UserRegister, db: AsyncSession = Depends(get_db)):
        try:
        
            if user_data.user_rol not in [ProfilesEnum.M.value, ProfilesEnum.P.value]:
                raise CantRegisterAdminError("No te puedes registar como administrador. ", 400)
        
            existeRol: bool = await self.__roles_repository.get_user_role(user_data.user_rol, db)

            if not existeRol:
                raise RolNotFoundError("Loco, no existe el rol que me mandaste. Mandame uno correctamente. ", 400)
            
            user: UserLogin = UserLogin(username = user_data.username, password = user_data.password)

            # Lo busco por username pero no quiero tocar la firma porque se me olvido donde más lo llamo y no quiero hacer más pruebas jeje
            existeUser = await self.__user_repository.get_user(user, db)

            if existeUser is not None:
                raise UserCreatedError("Ya existe un usuario creado con ese username, cambia de usuario para poder registrarte. ", 400)

            existeEmailRegistrado = await self.__user_repository.get_user_by_email(user_data.email, db)

            if existeEmailRegistrado is not None: 
                raise EmailUsedError("El email ya se encuentra utilizado. Por favor utilice otro email. ", 400)

            # Crear usuario
            new_user = Users(
                username=user_data.username,
                password=self.__hash_password(user_data.password),
                email=user_data.email,
                user_rol=user_data.user_rol,
                created_at=datetime.now()
            )
            
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            
            return {
                "message": "User created successfully",
                "user_id": new_user.id_user,
                "username": new_user.username
            }
    
        except IError as e:
            await db.rollback()
            raise HTTPException(status_code=e.http_code, detail=str(e))
        
        except Exception as ex:
            """Solo para excepciones no contraladas. 
            Siempre deberíamos usar una interfaz común, 
            como en nuestro caso de arriba que somos facheros. """
            
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"Algo ha salido mal. Comuniquese con sistemas. {ex}")

    async def authenticate_user(self, credentials: UserLogin, db: AsyncSession = Depends(get_db)) -> UserResponse:
        """Autenticar usuario y generar token"""
        # Buscar usuario
        user = await self.__user_repository.get_user(credentials, db)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username o contraseña equivocada. ",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar password
        if not self.__verify_password(credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Haz enviado un username o contraseña incorrecta. ",
                headers={"WWW-Authenticate": "Bearer"},
            )
        

        await self.__jwt_service.set_all_tokens_as_invalid(user.id_user, db)

        return await self.__jwt_service.create_access_token(user, db)


    async def reauthenticate_user(self, refresh_model: RefreshModel, db: AsyncSession = Depends(get_db)) -> UserResponse:
        refresh_token: RefreshToken | None =  await self.__refresh_token_repo.get_active_refresh_token(refresh_model.id_user, db)

        if (refresh_token is not None and refresh_token.refresh_token != refresh_model.refresh_token):
            raise RefreshTokenInvalidError(f"El token enviado no corresponde al último válidado por el sistema.", 403)
        
        return await self.__jwt_service.create_if_reathenticate(refresh_model, db)
        


    def __hash_password(self,password: str) -> str:
        """Hashear password"""
        return self.__pwd_context.hash(password)

    def __verify_password(self,plain_password: str, hashed_password: str) -> bool:
        """Verificar password"""
        return self.__pwd_context.verify(plain_password, hashed_password)

