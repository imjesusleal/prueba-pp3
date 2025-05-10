from models.electricidad import Electricidad
from repository import electricidad_repo
from sqlalchemy.ext.asyncio import AsyncSession

async def get_all(db: AsyncSession) -> list[Electricidad]:
    return await electricidad_repo.get_all(db)

async def get(id: int, db: AsyncSession) -> Electricidad:
    return await electricidad_repo.get(id, db)