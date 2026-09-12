from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
    )
    stock: int = Field(
        ge=0,
    )
    category_id: int   

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

    price: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    stock: int | None = Field(
        default=None,
        ge=0,
    )

    category_id: int | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    stock: int
    category_id: int

    model_config = ConfigDict(
        from_attributes=True
    )