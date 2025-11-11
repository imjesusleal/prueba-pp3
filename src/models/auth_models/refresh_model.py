from pydantic import BaseModel

class RefreshModel(BaseModel):
    refresh_token: str
    id_user: int
