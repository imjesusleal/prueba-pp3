from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from services.auth_services import AuthServices
from models.auth_models.user_register import UserRegister
from models.auth_models.token_response import TokenResponse
from models.auth_models.user_login import UserLogin 



class AuthRouter:
    '''
        Router para registrar y autenticar.
    '''
    def __init__(self): 

        self.__auth_service = AuthServices()

        self.router = APIRouter(prefix="/auth", tags=["authentication"])
        self.router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)(self.register)
        self.router.post("/login", response_model=TokenResponse)(self.login)

    # Endpoints
    async def register(self, user_data: UserRegister, db: AsyncSession = Depends(get_db)):
        """Registrar nuevo usuario"""
        return await self.__auth_service.register_user(user_data, db)
    
    async def login(self, credentials: UserLogin, db: AsyncSession = Depends(get_db)):
        """Login de usuario - retorna token JWT"""
        return await self.__auth_service.authenticate_user(credentials, db)
    

auth_router = AuthRouter()