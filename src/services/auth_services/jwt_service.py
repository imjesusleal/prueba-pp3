import uuid
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from db.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException

from db.entities.refresh_token import RefreshToken
from db.entities.users import Users
from errors.users.user_not_found_error import UserNotFoundError
from models.auth_models.refresh_model import RefreshModel
from models.auth_models.token_response import UserResponse
from repository.refresh_token import RefreshTokenRepo
from repository.users import UserRepository

__SECRET_KEY = os.getenv("SECRET_KEY")
__ALGORITHM = "HS256"
__AUTH_SCHEME = OAuth2PasswordBearer(tokenUrl="/auth/login")
__ACCESS_TOKEN_EXPIRE_MINUTES = 1440

class JwtService:

    __SECRET_KEY = os.getenv("SECRET_KEY")
    __ALGORITHM = "HS256"
    __ACCESS_TOKEN_EXPIRE_MINUTES = 1440
    __AUTH_SCHEME = OAuth2PasswordBearer(tokenUrl="/auth/login")

    def __init__(self, db:AsyncSession):
        self.__refresh_token_repo = RefreshTokenRepo(db)
        self.__user_repo = UserRepository(db)
        self._db = db

    async def get_current_user(self, token: str = Depends(__AUTH_SCHEME)): 
        try:
            payload = jwt.decode(token, self.__SECRET_KEY,self.__ALGORITHM)
            user_id: int = payload.get("id_user")

            if user_id is None:
                raise HTTPException(status_code=401, detail="Token inválido")
            
            return {"id_user": user_id}  
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido")

    async def create_access_token(self, user: Users, expires_delta: Optional[timedelta] = None) -> UserResponse:
        """
            Genera el token JWT que se le entrega a cada usuario con login exitoso
        """
        to_encode = {"sub": user.username, "id_user": user.id_user, "user_rol": user.user_rol}
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=self.__ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        jsonToken = jwt.encode(to_encode, self.__SECRET_KEY, algorithm=self.__ALGORITHM)

        refresh_token = await self.__get_refresh_token(user.id_user, jsonToken)

        return UserResponse(access_token=jsonToken, refresh_token=refresh_token, username=user.username, id_user=user.id_user, user_rol = user.user_rol)
    
    async def create_if_reathenticate(self, refresh_model: RefreshModel) -> UserResponse:
        await self.__refresh_token_repo.set_token_as_invalid(refresh_model)

        user = await self.__user_repo.get_user_by_id(refresh_model.id_user, True)

        if user is None:
            raise UserNotFoundError("El usuario informado no ha sido encontrado. ", 400)

        return await self.create_access_token(user)
    
    async def set_all_tokens_as_invalid(self, id_user) -> None:
        await self.__refresh_token_repo.set_all_tokens_as_invalid(id_user)
    
    async def __get_refresh_token(self, id_user: int,access_token: str) -> str:
        refresh_token_repo:RefreshTokenRepo = RefreshTokenRepo(self._db)
        last_refresh_token = await refresh_token_repo.get_active_refresh_token(id_user)
        
        if last_refresh_token is None:
            hoy = datetime.now()
            valido_hasta = hoy + timedelta(days=60)
            new_token = uuid.uuid4()
            refresh_token = RefreshToken(id_user=id_user,
                                        access_token=access_token,
                                        refresh_token = str(new_token), 
                                        is_used = 0, 
                                        valid_until= valido_hasta, 
                                        created_at= datetime.now(), 
                                        modified_at=datetime.now())
            await refresh_token_repo.create_refresh_token(refresh_token)
            return str(new_token)

        return last_refresh_token.access_token
    

async def get_current_user(
    token: str = Depends(__AUTH_SCHEME),
    db: AsyncSession = Depends(get_db)
) -> Users:
    try:
        payload = jwt.decode(token, __SECRET_KEY, algorithms=[__ALGORITHM])
        user_id = payload.get("id_user")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        user_repo = UserRepository(db)
        user: Users = await user_repo.get_user_by_id(user_id)
        return user
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")