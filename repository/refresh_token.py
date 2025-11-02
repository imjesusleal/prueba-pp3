from datetime import datetime
from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.refresh_token import RefreshToken
from typing import Optional

from errors.refresh_token.refresh_token_created_error import RefreshTokenCreatedError
from errors.refresh_token.refresh_token_invalid import RefreshTokenInvalidError
from models.auth_models.refresh_model import RefreshModel


class RefreshTokenRepo:

    async def get_active_refresh_token(self, id_user: int, db: AsyncSession = Depends(get_db)) -> Optional[RefreshToken]:
        query = select(RefreshToken).filter((RefreshToken.id_user == id_user) & (RefreshToken.is_used == False) & (RefreshToken.valid_until >= datetime.now())) 
        res = await db.execute(query)
        refresh_token = res.scalars().first()
        return refresh_token

    async def create_refresh_token(self, refresh_token: RefreshToken, db: AsyncSession = Depends(get_db)) -> Optional[RefreshToken]: 
        try:
            db.add(refresh_token)
            await db.commit()
            await db.refresh(refresh_token)
            return refresh_token
        except Exception as ex:
            raise RefreshTokenCreatedError(f"No se pudo crear el token de refrescamiento por esta razón: {ex}")
        
    async def set_token_as_invalid(self, refresh_token: RefreshToken, db: AsyncSession = Depends(get_db)) -> None:
        query = select(RefreshToken).filter((RefreshToken.id_user == refresh_token.id_user) & (RefreshToken.refresh_token == refresh_token.refresh_token))
        res = await db.execute(query)
        refresh_token = res.scalars().first()

        if refresh_token is not None: 
            refresh_token.is_used = 1
        
        await db.commit()
        await db.refresh(refresh_token)

    async def set_all_tokens_as_invalid(self, id_user, db: AsyncSession = Depends(get_db)) -> None:
        query = select(RefreshToken).filter((RefreshToken.id_user == id_user) & (RefreshToken.is_used == 0))
        res = await db.execute(query)
        tokens = res.scalars()

        for token in tokens:
            token.is_used = 1

        await db.commit()