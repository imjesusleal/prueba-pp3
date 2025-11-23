from pydantic import BaseModel

from services.profiles.enums.profiles_enums import ProfilesEnum

class UserResponse(BaseModel):
    access_token: str
    refresh_token: str
    id_user: int
    username: str
    user_rol: ProfilesEnum

