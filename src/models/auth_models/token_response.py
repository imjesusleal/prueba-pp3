from pydantic import BaseModel

class UserResponse(BaseModel):
    access_token: str
    refresh_token: str
    id_user: int
    username: str

