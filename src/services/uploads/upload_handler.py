import base64
import os
from pathlib import Path
import shutil
import uuid
from fastapi import Depends, UploadFile

from db.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from db.entities.users import Users
from repository.users import UserRepository

from errors.users.user_not_found_error import UserNotFoundError
from services.profiles.enums.profiles_enums import ProfilesEnum

class UploadHandler:

    __UPLOAD_DIR = "files"
    __BASE_PATH = Path(__file__).resolve().parent.parent.parent
    __FULL_PATH = Path.joinpath(__BASE_PATH, __UPLOAD_DIR)
    os.makedirs(__FULL_PATH,exist_ok=True)

    def __init__(self):
        self.__user_repo = UserRepository()

    async def upload_img(self, id_user: int,  file: UploadFile, db: AsyncSession = Depends(get_db)) -> str: 

        user: Users = await self.__user_repo.get_user_with_profile(id_user, db)

        if not user:
            raise UserNotFoundError("El usuario no ha sido encontrado", 404)


        file_name_no_extension = file.filename.split('.')

        stamp = uuid.uuid4()
        full_filename = f'{file_name_no_extension[0]}_{stamp}.{file_name_no_extension[1]}'
        file_path = self.__FULL_PATH / full_filename

        with file_path.open("wb") as buffer: 
            shutil.copyfileobj(file.file, buffer)

        
        if user.user_rol == ProfilesEnum.M.value:
            last_img = user.medico.img_name
            self.__clear_img(last_img)
            user.medico.img_name = full_filename
        elif user.user_rol == ProfilesEnum.P.value:
            last_img = user.paciente.img_name
            self.__clear_img(last_img)
            user.paciente.img_name = full_filename

        await db.commit()
        
        return full_filename


    def pdf_to_bytes(self, pdf_name: str) -> bytes:
        pdf_filepath = Path(self.__FULL_PATH) / pdf_name
        try:
            with open(pdf_filepath, 'rb') as f:
                pdf_bytes = f.read()
            return pdf_bytes
        except FileNotFoundError:
            print(f"Error: El archivo '{pdf_filepath}' no ha sido encontrado.")
            return None
        except Exception as e:
            print(f"Ha ocurrido un error: {e}")
            return None


    def __clear_img(self, img_name: str): 
        if not img_name:
            return 
        
        file_path = Path(self.__FULL_PATH) / img_name
        try:
            os.remove(file_path)
        except:
            ## Si no la encuentro ps ya fue, no borro nada ni rompo nada, solo grabo la que me pasaron y la piso en la base.
            return
        


        