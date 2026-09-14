from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.address import Address

def get_addresses(
        db: Session,
        user_id: int
):
    statement = (
        select(Address)
        .where(Address.user_id == user_id)
        .order_by(
            Address.is_default.desc(),
            Address.id.desc()
        )
    )

    return list(db.scalars(statement).all())

def get_address(
    db: Session,
    user_id: int,
    address_id: int,
):
    statement = select(Address).where(
        Address.id == address_id,
        Address.user_id == user_id,
    )

    return db.scalar(statement)

def create_address(
    db: Session,
    user_id: int,
    data,
):
    if data.is_default:
        statement = select(Address).where(
            Address.user_id == user_id
        )

        existing_addresses = db.scalars(
            statement
        ).all()

        for address in existing_addresses:
            address.is_default = False

    address = Address(
        user_id=user_id,
        full_name=data.full_name,
        phone=data.phone,
        address_line=data.address_line,
        city=data.city,
        state=data.state,
        postal_code=data.postal_code,
        country=data.country,
        is_default=data.is_default,
    )

    db.add(address)
    db.commit()
    db.refresh(address)

    return address

def update_address(
    db: Session,
    user_id: int,
    address_id: int,
    data,
):
    address = get_address(
        db,
        user_id,
        address_id,
    )

    if address is None:
        return None

    update_data = data.model_dump(
        exclude_unset=True
    )

    if update_data.get("is_default") is True:

        statement = select(Address).where(
            Address.user_id == user_id,
            Address.id != address_id,
        )

        other_addresses = db.scalars(
            statement
        ).all()

        for other in other_addresses:
            other.is_default = False

    for field, value in update_data.items():
        setattr(address, field, value)

    db.commit()
    db.refresh(address)

    return address

def delete_address(
    db: Session,
    user_id: int,
    address_id: int,
):
    address = get_address(
        db,
        user_id,
        address_id,
    )

    if address is None:
        return False

    db.delete(address)
    db.commit()

    return True