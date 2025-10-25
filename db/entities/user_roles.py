from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class UserRoles(SQLModel, table=True):
    __tablename__ = "users_roles"
    
    id_users_roles: Optional[int] = Field(default=None, primary_key=True)
    rol: str = Field(max_length=1)
    description: str = Field(max_length=255)
    created_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)