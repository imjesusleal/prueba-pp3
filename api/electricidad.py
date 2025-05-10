from fastapi import APIRouter, Depends
from db.db import get_db
from services import electricidad_service
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/electricidad", tags=["electricidad"])

@router.get("/getAll")
async def get_all_electricidad(db: AsyncSession = Depends(get_db)):
    return await electricidad_service.get_all(db)

@router.get("/get/{id}")
async def get_electricidad(id: int, db: AsyncSession = Depends(get_db)):
    return await electricidad_service.get(id, db)