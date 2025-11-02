from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from models.auth_models.refresh_model import RefreshModel
from services.auth_services.auth_services import AuthServices
from models.auth_models.user_register import UserRegister
from models.auth_models.token_response import UserResponse
from models.auth_models.user_login import UserLogin 


class AuthRouter:
    '''
        Router para registrar y autenticar.
    '''
    def __init__(self):
        self.__auth_service = AuthServices()


        self.router = APIRouter(prefix="/auth", tags=["authentication"])
        self.router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)(self.register)
        self.router.post("/login", response_model=UserResponse)(self.login)
        self.router.post("/reauthenticate", response_model=UserResponse)(self.reauthenticate)

    # Endpoints
    async def register(self, user_data: UserRegister, db: AsyncSession = Depends(get_db)):
        """Registrar nuevo usuario"""
        return await self.__auth_service.register_user(user_data, db)
    
    async def login(self, credentials: UserLogin, db: AsyncSession = Depends(get_db)) -> UserResponse:
        """Login de usuario - retorna token JWT"""
        return await self.__auth_service.authenticate_user(credentials,db)
    
    async def reauthenticate(self, refresh_model: RefreshModel,db: AsyncSession = Depends(get_db)):
        return await self.__auth_service.reauthenticate_user(refresh_model,db)
    

auth_router = AuthRouter()