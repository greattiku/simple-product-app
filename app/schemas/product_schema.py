from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CreateProduct(BaseModel):
    name: str
    description: str
    cost: float
    pictures: list[str]


class UpdateProduct(BaseModel):
    name: str | None = None
    description: str | None = None
    cost: float | None = None
    pictures: list[str] | None = None


class ProductDto(BaseModel):
    id: int
    name: str
    description: str
    cost: float
    pictures: list[str]
    created_at: datetime
    updated_at: datetime
    admin_id: int 
    model_config = ConfigDict(from_attributes=True)


class ProductResponse(BaseModel):
    message: str
    product: ProductDto

