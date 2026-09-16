from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

class PaymentCreate(BaseModel):
    order_id: int

class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: Decimal
    currency: str
    status: str
    provider: str
    provider_payment_id: str | None
    transaction_reference: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class PaymentVerify(BaseModel):
    provider_payment_id: str