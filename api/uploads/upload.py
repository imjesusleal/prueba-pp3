from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from db.db import get_db
from services.auth_services.jwt_service import jwt_service
from sqlalchemy.ext.asyncio import AsyncSession

from services.uploads.upload_handler import UploadHandler

class UploadRouter:



    def __init__(self):

        self.__upload_handler = UploadHandler()

        self.router = APIRouter(prefix="/uploads", tags=["uploads`"])
        self.router.post("/save_img", status_code=201)(self.upload_image)

    async def upload_image(self, file: UploadFile = File(), 
                           db: AsyncSession = Depends(get_db), 
                           current_user: dict = Depends(jwt_service.get_current_user)):

        if file.content_type not in ["application/pdf"]:
           raise HTTPException(status_code=400, detail="Solo PDFs permitidos")

        if not current_user["id_user"]:
            raise HTTPException(status_code=400, detail="Se debe enviar el identificador del usuario para guardar una imagen.")

        await self.__upload_handler.upload_img(current_user["id_user"], file, db)

    
router = UploadRouter()