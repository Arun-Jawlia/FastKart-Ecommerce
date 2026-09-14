from sqlalchemy import ForeignKey, UniqueConstraint,
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class CartItem(Base):
    __tablename__='cart_items'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index = True
    )

    cart_id: Mapped[int] = mapped_column(
        ForeignKey("carts.id"),
        index = True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id'),
        index= True
    )

    quantity: Mapped[int] = mapped_column(
        default = 1
    )

    cart = relationship(
        "Cart",
        back_populates = "items"
    )
    product = relationship(
        'Product'
    )

    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "product_id",
            name = 'uq_cart_product'
        )
    )