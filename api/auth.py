#endpoints de autentificación
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from services import auth_services
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["authentication"])

# Schemas
class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr
    user_rol: int

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    id_user: int
    username: str

# Endpoints
@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    """Registrar nuevo usuario"""
    return await auth_services.register_user(user_data, db)

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login de usuario - retorna token JWT"""
    return await auth_services.authenticate_user(credentials, db)

@router.post("/login/form", response_model=TokenResponse)
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Login usando OAuth2 form (para Swagger UI)"""
    credentials = UserLogin(username=form_data.username, password=form_data.password)
    return await auth_services.authenticate_user(credentials, db)

@router.get("/me")
async def get_current_user(
    current_user: dict = Depends(auth_services.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obtener información del usuario autenticado"""
    return current_user