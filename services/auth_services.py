from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
#lógica de negocio
from repository.medify_repositories import (
    get_user_by_username, 
    get_user_by_email
)
from models.medify_models import Users
from db.db import get_db

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "dbae28de74ae9ff9ee92db82b92774ab6beeb5cb9cb96903e1e6d7a67fe19bd4")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# pwd_context = CryptContext(
#     schemes=["argon2"], 
#     deprecated="auto",
#     bcrypt__rounds=10,
#     bcrypt__ident="2b"
# )
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/form")

#Esta función va para el endpoint de registro de usuario y guarda la contraseña ya hasheada
def hash_password(password: str) -> str:
    """Hashear password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:#compara la contraseña del usuario con la hash guardado
    """Verificar password"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):#genera el token JWT que se le entrega a cada usuario con login exitoso
    """Crear token JWT"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# =======Servicios principales
async def register_user(user_data, db: AsyncSession):
    try:
        # Verificaciones existentes...
        
        # Crear usuario
        new_user = Users(
            username=user_data.username,
            password=hash_password(user_data.password),
            email=user_data.email,
            user_rol=user_data.user_rol,
            created_at=datetime.utcnow()
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        return {
            "message": "User created successfully",
            "user_id": new_user.id_user,
            "username": new_user.username
        }
    except Exception as e:
        await db.rollback()
        print(f"Error en register: {e}")  # Ver en terminal
        raise HTTPException(status_code=500, detail=str(e))

async def authenticate_user(credentials, db: AsyncSession):
    """Autenticar usuario y generar token"""
    # Buscar usuario
    user = await get_user_by_username(credentials.username, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar password
    if not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token
    access_token = create_access_token(
        data={"sub": user.username, "id_user": user.id_user}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id_user": user.id_user,
        "username": user.username
    }

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """Obtener usuario actual desde token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id_user: int = payload.get("id_user")
        
        if username is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = await get_user_by_username(username, db)
    
    if user is None:
        raise credentials_exception
    
    return {
        "id_user": user.id_user,
        "username": user.username,
        "email": user.email,
        "user_rol": user.user_rol
    }