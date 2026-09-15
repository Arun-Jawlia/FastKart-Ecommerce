from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class InventoryTransaction(Base):
    __tablename__ = 'inventory_transactions'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id'),
        index = True
    )

    quantity_change: Mapped[int] = mapped_column(
        Integer
    )

    previous_quantity: Mapped[int] = mapped_column(
        Integer
    )
    new_quantity: Mapped[int] = mapped_column(
        Integer
    )
    transcation_type: Mapped[str] = mapped_column(
        Text,
        nullable = True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default = datetime.utcnow,
    )

    product = relationship("Product")