from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal

class OrderResponse(BaseModel):
    id: int
    status: str
    subtotal: Decimal
    total: Decimal
    created_at: datetime
    items: list[OrderItemResponse]

class OrderStatusUpdate(BaseModel):
    status: str