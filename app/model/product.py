from datetime import datetime, timezone


from sqlmodel import ARRAY, Column, Field, SQLModel, String


class Product(SQLModel, table = True):
    __tablename__ = "products"

    id:int | None = Field(default=None, primary_key=True)
    name:str
    description:str
    cost:float
    pictures: list[str] = Field(sa_column=Column(ARRAY(String)))
    admin_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


