from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductUpdate
)

def create_product(
        db: Session, 
        product_data: ProductCreate) -> Product:
    product = Product(
        name = product_data.name,
        description = product_data.description,
        price = product_data.name,
        stock= product_data.price,
        category_id = product_data.category_id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product

def get_products(
    db: Session
)-> list[Product]:
    statement = select(Product)

    return list(
        db.scalars(statement).all()
    )

def get_product_by_id(
        db: Session,
        product_id: int
) -> Product | None:
    return db.get(Product, product_id)


def update_product(
        db: Session,
        product: Product,
        product_data: ProductUpdate
) -> Product | None:
    
    update_data = product_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(update_data, field, value)

    db.commit()
    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product: Product,
) -> None:

    db.delete(product)
    db.commit()


