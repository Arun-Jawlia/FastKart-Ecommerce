from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Numeric,
    String
)

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Payment(Base):
    __tablename__='payments'

    id: Mapped[int] = mapped_column(
        primary_key= True,
        index = True
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        unique=True,
        index= True
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="INR",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
        index=True,
    )
    provider: Mapped[str] = mapped_column(
        String(30),
        default="MOCK",
    )
    provider_payment_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    transaction_reference: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )

    idempotency_key: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    order = relationship("Order")