from decimal import Decimal
from pydantic import BaseModel, Field

class CartItemAdd(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(ge=1)

class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    price: Decimal
    quantity: int
    subtotal: Decimal


class CartResponse(BaseModel):
    id: int
    items: list[CartItemResponse]
    total: Decimal

