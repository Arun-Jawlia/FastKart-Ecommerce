from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        index=True,
    )

    product_name: Mapped[str] = mapped_column(
        String(150),
    )

    quantity: Mapped[int] = mapped_column()

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
    )

    order = relationship(
        "Order",
        back_populates="items",
    )

    product = relationship("Product")