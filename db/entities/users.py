from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Users(SQLModel, table=True):
    __tablename__= "users"

    id_user: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=100, unique=True)
    password: str = Field(max_length=255)
    email: str = Field(max_length=255, unique=True)
    user_rol: Optional[int] = Field(default=None, foreign_key="users.id_user")
    created_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)