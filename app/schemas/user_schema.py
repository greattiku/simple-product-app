

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.model.user import UserRole


class CreateUser(BaseModel):
    first_name: str 
    last_name: str
    email: str 
    phone_number: str | None = None
    password:str

class UpdateUser(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    password: str | None = None

class UpdateUserRole(BaseModel):
    role: UserRole

class UserDto(BaseModel):
    id: int
    first_name: str 
    last_name: str
    email: str 
    phone_number: str | None = None
    is_active: bool = False 
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    message: str
    user: UserDto

