from datetime import datetime
from pydantic import BaseModel, Field

class StockUpdate(BaseModel):
    quantity: int = Field(gt=0)
    reason: str | None = Field(default = None, max_length = 500)

class StockSet(BaseModel):
    quantity: int = Field(
        ge=0,
    )

    reason: str | None = Field(
        default=None,
        max_length=500,
    )    

class InventoryTransactionResponse(BaseModel):
    id: int
    product_id: int
    quantity_change: int
    previous_quantity: int
    new_quantity: int
    transaction_type: str
    reason: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }