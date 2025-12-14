from datetime import datetime
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.entities.refresh_token import RefreshToken
from typing import Optional

from errors.refresh_token.refresh_token_created_error import RefreshTokenCreatedError

class RefreshTokenRepo:

    def __init__(self, db: AsyncSession):
        self._db = db
    
    async def get_active_refresh_token(self, id_user: int) -> Optional[RefreshToken]:
        query = select(RefreshToken).filter((RefreshToken.id_user == id_user) & (RefreshToken.is_used == False) & (RefreshToken.valid_until >= datetime.now())) 
        res = await self._db.execute(query)
        refresh_token = res.scalars().first()
        return refresh_token

    async def create_refresh_token(self, refresh_token: RefreshToken) -> Optional[RefreshToken]: 
        try:
            self._db.add(refresh_token)
            await self._db.commit()
            await self._db.refresh(refresh_token)
            return refresh_token
        except Exception as ex:
            raise RefreshTokenCreatedError(f"No se pudo crear el token de refrescamiento por esta razón: {ex}", 404)
        
    async def set_token_as_invalid(self, refresh_token: RefreshToken) -> None:
        query = select(RefreshToken).filter((RefreshToken.id_user == refresh_token.id_user) & (RefreshToken.refresh_token == refresh_token.refresh_token))
        res = await self._db.execute(query)
        refresh_token = res.scalars().first()

        if refresh_token is not None: 
            refresh_token.is_used = 1
        
        await self._db.commit()
        await self._db.refresh(refresh_token)

    async def set_all_tokens_as_invalid(self, id_user) -> None:
        query = select(RefreshToken).filter((RefreshToken.id_user == id_user) & (RefreshToken.is_used == 0))
        res = await self._db.execute(query)
        tokens = res.scalars()

        for token in tokens:
            token.is_used = 1

        await self._db.commit()