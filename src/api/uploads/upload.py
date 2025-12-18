from pathlib import Path
from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, Response

from db.db import get_db
from db.entities.users import Users
from services.auth_services.jwt_service import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession

from services.uploads.upload_handler import UploadHandler


class UploadRouter:

    __ALLOWED_CONTENT_TYPES =  ["application/pdf", "image/jpeg", "image/jpg"]
    __ALLOWED_TYPES = ['pdf', 'jpg', 'jpeg']

    def __init__(self):

        self.router = APIRouter(prefix="/uploads", tags=["uploads"])
        self.router.post("/save_img", response_model=str,status_code=201)(self.upload_image)
        self.router.post("/download", response_class=Response, status_code=201)(self.download_profile_img)

    async def upload_image(self, file: UploadFile = File(), 
                           db: AsyncSession = Depends(get_db), 
                           current_user: Users = Depends(get_current_user)):

        if file.content_type not in self.__ALLOWED_CONTENT_TYPES:
           raise HTTPException(status_code=400, detail="Los archivos permitidos son pdfs, jpeg y jpg.")

        if not current_user.id_user:
            raise HTTPException(status_code=400, detail="Se debe enviar el identificador del usuario para guardar una imagen.")


        handler = UploadHandler(db)
        res =  await handler.upload_img(current_user.id_user, file)
        
        return res

    async def download_profile_img(self, img_name:str = Body(embed=True), db: AsyncSession = Depends(get_db),current_user: Users = Depends(get_current_user)): 

        if img_name.split(".")[1] not in self.__ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail="El archivo enviado no tiene una extensión permitida")

        handler = UploadHandler(db)
        pdf_bytes = handler.pdf_to_bytes(img_name)

        headers = {
        "Content-Disposition": f"attachment; filename={img_name}",
        "Content-Type": "image/jpeg"
        }

        return Response(content=pdf_bytes,headers=headers,media_type="image/jpeg")

    
router = UploadRouter()