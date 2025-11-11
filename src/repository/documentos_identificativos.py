from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.entities.documento_identificativo import DocumentoIdentificativo
from typing import List, Optional


async def get_all_documentos(db: AsyncSession = Depends(get_db)) -> List[DocumentoIdentificativo]:
    res = await db.execute(select(DocumentoIdentificativo))
    return res.scalars().all()

async def get_documento(id: int, db: AsyncSession = Depends(get_db)) -> Optional[DocumentoIdentificativo]:
    query = select(DocumentoIdentificativo).filter(DocumentoIdentificativo.id_documento == id)
    res = await db.execute(query)
    return res.scalars().first()

async def get_documento_by_tipo(tipo: str, db: AsyncSession = Depends(get_db)) -> Optional[DocumentoIdentificativo]:
    query = select(DocumentoIdentificativo).filter(DocumentoIdentificativo.tipo_documento == tipo)
    res = await db.execute(query)
    return res.scalars().first()