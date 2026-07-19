
from pydantic import BaseModel

from app.schemas.user_schema import UserDto


class LoginUser(BaseModel):
    email: str
    password:str

class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"
    user: UserDto


