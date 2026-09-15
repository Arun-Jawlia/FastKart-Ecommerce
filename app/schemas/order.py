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
    shipping_full_name: str
    shipping_phone: str
    shipping_address_line: str
    shipping_city: str
    shipping_state: str
    shipping_postal_code: str
    shipping_country: str

class OrderStatusUpdate(BaseModel):
    status: str

class CheckoutRequest(BaseModel):
    address_id: int