import uuid
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from db.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from db.entities.refresh_token import RefreshToken
from db.entities.users import Users
from errors.users.user_not_found_error import UserNotFoundError
from models.auth_models.refresh_model import RefreshModel
from models.auth_models.token_response import UserResponse
from repository.refresh_token import RefreshTokenRepo
from repository.users import UserRepository

class JwtService:

    __SECRET_KEY = os.getenv("SECRET_KEY")
    __ALGORITHM = "HS256"
    __ACCESS_TOKEN_EXPIRE_MINUTES = 60

    def __init__(self):
        self.__refresh_token_repo = RefreshTokenRepo()
        self.__user_repo = UserRepository()


    async def create_access_token(self, user: Users, db: AsyncSession = Depends(get_db), expires_delta: Optional[timedelta] = None) -> UserResponse:
        """
            Genera el token JWT que se le entrega a cada usuario con login exitoso
        """
        to_encode = {"sub": user.username, "id_user": user.id_user}
        expire = datetime.now() + (expires_delta or timedelta(minutes=self.__ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        jsonToken = jwt.encode(to_encode, self.__SECRET_KEY, algorithm=self.__ALGORITHM)

        refresh_token = await self.__get_refresh_token(user.id_user, jsonToken, db)

        return UserResponse(access_token=jsonToken, refresh_token=refresh_token, username=user.username, id_user=user.id_user)
    
    async def create_if_reathenticate(self, refresh_model: RefreshModel, db: AsyncSession = Depends(get_db)) -> UserResponse:
        await self.__refresh_token_repo.set_token_as_invalid(refresh_model, db)

        user = await self.__user_repo.get_user_by_id(refresh_model.id_user, db)

        if user is None:
            raise UserNotFoundError("El usuario informado no ha sido encontrado. ")

        return await self.create_access_token(user, db)
    
    async def set_all_tokens_as_invalid(self, id_user, db: AsyncSession = Depends(get_db)) -> None:
        await self.__refresh_token_repo.set_all_tokens_as_invalid(id_user,db)
    
    async def __get_refresh_token(self, id_user: int,access_token: str, db: AsyncSession = Depends(get_db)) -> str:
        refresh_token_repo:RefreshTokenRepo = RefreshTokenRepo()
        last_refresh_token = await refresh_token_repo.get_active_refresh_token(id_user, db)
        
        if last_refresh_token is None:
            hoy = datetime.now()
            valido_hasta = hoy + timedelta(days=60)
            new_token = uuid.uuid4()
            refresh_token = RefreshToken(id_user=id_user,
                                        access_token=access_token,
                                        refresh_token = new_token, 
                                        is_used = 0, 
                                        valid_until= valido_hasta, 
                                        created_at= datetime.now(), 
                                        modified_at=datetime.now())
            await refresh_token_repo.create_refresh_token(refresh_token, db)
            return str(new_token)

        return last_refresh_token.access_token
        
