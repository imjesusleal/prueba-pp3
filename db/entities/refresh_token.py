from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class RefreshToken(SQLModel, table=True):
    __tablename__= "refresh_token"

    id_token: int = Field(default=None, primary_key=True, )
    id_user: int = Field(default=None, foreign_key="users.id_user")
    refresh_token: str = Field(default=None)
    access_token: str = Field(default=None)
    is_used: bool = Field(default=None)
    valid_until: datetime = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)