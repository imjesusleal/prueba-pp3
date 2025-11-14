from pathlib import Path
from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, Response

from db.db import get_db
from services.auth_services.jwt_service import jwt_service
from sqlalchemy.ext.asyncio import AsyncSession

from services.uploads.upload_handler import UploadHandler


class UploadRouter:

    def __init__(self):

        self.__upload_handler = UploadHandler()

        self.router = APIRouter(prefix="/uploads", tags=["uploads"])
        self.router.post("/save_img", response_model=str,status_code=201)(self.upload_image)
        self.router.post("/download", response_class=Response, status_code=201)(self.download_profile_img)

    async def upload_image(self, file: UploadFile = File(), 
                           db: AsyncSession = Depends(get_db), 
                           current_user: dict = Depends(jwt_service.get_current_user)):

        if file.content_type not in ["application/pdf"]:
           raise HTTPException(status_code=400, detail="Solo PDFs permitidos")

        if not current_user["id_user"]:
            raise HTTPException(status_code=400, detail="Se debe enviar el identificador del usuario para guardar una imagen.")

        res =  await self.__upload_handler.upload_img(current_user["id_user"], file, db)
        
        return res

    async def download_profile_img(self, img_name:str = Body(embed=True), current_user: dict = Depends(jwt_service.get_current_user)): 

        if img_name.split(".")[1] != "pdf":
            raise "mal envio"

        pdf_bytes = self.__upload_handler.pdf_to_bytes(img_name)

        headers = {
        "Content-Disposition": f"attachment; filename={img_name}",
        "Content-Type": "application/pdf"
        }

        return Response(content=pdf_bytes,headers=headers,media_type="application/pdf")

    
router = UploadRouter()