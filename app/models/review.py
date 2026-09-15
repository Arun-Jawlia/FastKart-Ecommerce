from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(
        primary_key = True,
        index = True
    )

    user_id : Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        index =True
    )
    product_id : Mapped[int] = mapped_column(
        ForeignKey('products.id'),
        index =True
    )
    rating: Mapped[int] = mapped_column(
        Integer
    )

    comment: Mapped[str] = mapped_column(
        Text, 
        nullable = True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default = datetime.utcnow
    )

    user = relationship('User')
    product = relationship("Product")

    __tablename__ = (
        UniqueConstraint(
            'user_id',
            "product_id",
            name = 'uq_user_product_review'
        )
    )