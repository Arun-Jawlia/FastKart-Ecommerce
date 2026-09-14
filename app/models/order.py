from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(
        primary_key = True,
        index = True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        index= True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
        index=True,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
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

    user = relationship("User")
    items = relationship(
        "OrderItem",
        back_populates = 'order',
        cascade="all, delete-orphan"
    )