from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os

from models.auth_models.user_login import UserLogin
from models.auth_models.user_register import UserRegister
from repository.user_roles import UsersRolesRepository
from repository.users import UserRepository
from db.entities.users import Users
from db.db import get_db

class AuthServices: 

    def __init__(self):
        self.__roles_repository = UsersRolesRepository()
        self.__user_repository = UserRepository()

    # Configuración de seguridad
    __SECRET_KEY = os.getenv("SECRET_KEY")
    __ALGORITHM = "HS256"
    __ACCESS_TOKEN_EXPIRE_MINUTES = 60


    __pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
    __oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/form")

    # =======Servicios principales
    async def register_user(self, user_data: UserRegister, db: AsyncSession = Depends(get_db)):
        try:
            # Verificaciones existentes...
        
            existeRol: bool = await self.__roles_repository.get_user_role(user_data.user_rol, db)

            if not existeRol:
                raise Exception("Loco, no existe el rol que me mandaste. Mandame uno correctamente")
            
            user: UserLogin = UserLogin(username = user_data.username, password = user_data.password)


            existeUser = await self.__user_repository.get_user(user, db)

            if existeUser is not None:
                raise Exception("Loco ya existe ese usuario, no te podes registrar con ese!")

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
        except Exception as e:
            await db.rollback()
            print(f"Error en register: {e}")  # Ver en terminal
            raise HTTPException(status_code=500, detail=str(e))

    async def authenticate_user(self, credentials: UserLogin, db: AsyncSession):
        """Autenticar usuario y generar token"""
        # Buscar usuario
        user = await self.__user_repository.get_user(credentials, db)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar password
        if not self.__verify_password(credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Crear token
        access_token = self.__create_access_token(
            data={"sub": user.username, "id_user": user.id_user}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "id_user": user.id_user,
            "username": user.username
        }

        #Esta función va para el endpoint de registro de usuario y guarda la contraseña ya hasheada
    def __hash_password(self,password: str) -> str:
        """Hashear password"""
        return self.__pwd_context.hash(password)

    def __verify_password(self,plain_password: str, hashed_password: str) -> bool:#compara la contraseña del usuario con la hash guardado
        """Verificar password"""
        return self.__pwd_context.verify(plain_password, hashed_password)

    def __create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):#genera el token JWT que se le entrega a cada usuario con login exitoso
        """Crear token JWT"""
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta or timedelta(minutes=self.__ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.__SECRET_KEY, algorithm=self.__ALGORITHM)
