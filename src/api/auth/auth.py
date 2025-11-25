from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse
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
    
    async def login(self, response: Response, credentials: UserLogin, db: AsyncSession = Depends(get_db)) -> UserResponse:
        """Login de usuario - retorna token JWT"""
        
        res = await self.__auth_service.authenticate_user(credentials,db)
        
        json_res = JSONResponse(content=res.model_dump())

        # Setear cookies en ese response
        self.__create_cookies(res, json_res)

        return json_res
        
    
    async def reauthenticate(self,request: Request, db: AsyncSession = Depends(get_db)):
        refresh_model = self.__get_cookies(request)
        res = await self.__auth_service.reauthenticate_user(refresh_model, db)
        
        json_res = JSONResponse(content=res.model_dump())

        # Setear cookies en ese response
        self.__create_cookies(res, json_res)

        return json_res
    
    
    def __create_cookies(self, res: UserResponse, response: Response):
        response.set_cookie(
            key="refresh_token",
            value=res.refresh_token,
            httponly=True,
            secure=True,
            samesite="none",
            path='/',
            max_age=60*60*24*7
        )
        
        response.set_cookie(
            key="id_user",
            value=str(res.id_user),
            httponly=True,
            secure=True,
            samesite="none",
            max_age=60 * 60 * 24 * 7,
            path="/"
        )
    
    def __get_cookies(self, request: Request) -> RefreshModel:
        refresh_token = request.cookies.get("refresh_token")
        id_user = request.cookies.get("id_user")
        
        return RefreshModel(refresh_token=refresh_token, id_user=id_user)
        
    

auth_router = AuthRouter()