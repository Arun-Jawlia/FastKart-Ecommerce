from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(
        primary_key = True,
        index = True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        index = True
    )

    full_name : Mapped[str] = mapped_column(
        String(100)
    )

    phone: Mapped[str] = mapped_column(
        String(20)
    )

    address_line: Mapped[str] = mapped_column(
        String(255)
    )

    city: Mapped[str] = mapped_column(
        String(100)
    )

    state: Mapped[str] = mapped_column(
        String(100)
    )

    postal_code: Mapped[str] = mapped_column(
        String(20)
    )

    country: Mapped[str] = mapped_column(
        String(100),
        default="India",
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    user = relationship(
        "User",
        back_populates = 'addresses',  
    )