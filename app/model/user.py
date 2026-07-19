

from datetime import datetime, timezone
from enum import Enum

from sqlmodel import  Field, SQLModel

class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"


class User(SQLModel, table = True):
    __tablename__ = 'users'

    id: int |None = Field(default = None, primary_key= True)
    first_name: str 
    last_name: str
    email: str = Field(unique= True)
    phone_number: str | None = None
    password: str
    is_active: bool = Field(default=False) 
    role: UserRole = UserRole.CUSTOMER
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

