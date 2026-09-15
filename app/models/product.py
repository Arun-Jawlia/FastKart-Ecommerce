from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from decimal import Decimal

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        primary_key = True,
        index = True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
    )

    stock: Mapped[int] = mapped_column(
        default=0,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        index=True,
    )

    category = relationship(
        "Category",
        back_populates="products",
    )

    low_stock_threshold: Mapped[int] = mapped_column(
    default=5,
    )