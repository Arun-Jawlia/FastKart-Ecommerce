from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.inventory_transaction import InventoryTransaction
from app.models.product import Product


def restock_product (
        db: Session,
        product_id: int,
        quantity: int,
        reason: str | None = None
): 
    product = db.get(Product, product_id)

    if product is None: 
        return None, "PRODUCT_NOT_FOUND"

    previous_quanity = product.stock

    product.stock += quantity

    transaction = InventoryTransaction(
        product_id = product.id,
        quantity_change = quantity,
        previous_quanity = previous_quanity,
        new_quantity = product.stock,
        transaction_type = 'RESTOCK',
        reason = reason
    )

    db.add(transaction)
    db.commit()
    db.refresh(product)

    return product, None


def remove_stock(
    db: Session,
    product_id: int,
    quantity: int,
    reason: str | None = None,
):
    product = db.get(Product, product_id)

    if product is None:
        return None, "PRODUCT_NOT_FOUND"

    if quantity > product.stock:
        return None, "INSUFFICIENT_STOCK"

    previous_quantity = product.stock

    product.stock -= quantity

    transaction = InventoryTransaction(
        product_id=product.id,
        quantity_change=-quantity,
        previous_quantity=previous_quantity,
        new_quantity=product.stock,
        transaction_type="DAMAGE",
        reason=reason,
    )

    db.add(transaction)
    db.commit()

    db.refresh(product)

    return product, None

def set_stock(
    db: Session,
    product_id: int,
    quantity: int,
    reason: str | None = None,
):
    product = db.get(Product, product_id)

    if product is None:
        return None, "PRODUCT_NOT_FOUND"

    previous_quantity = product.stock

    change = quantity - previous_quantity

    product.stock = quantity

    transaction = InventoryTransaction(
        product_id=product.id,
        quantity_change=change,
        previous_quantity=previous_quantity,
        new_quantity=quantity,
        transaction_type="ADJUSTMENT",
        reason=reason,
    )

    db.add(transaction)
    db.commit()

    db.refresh(product)

    return product, None

def get_inventory_history(
    db: Session,
    product_id: int,
):
    statement = (
        select(InventoryTransaction)
        .where(
            InventoryTransaction.product_id
            == product_id
        )
        .order_by(
            InventoryTransaction.created_at.desc()
        )
    )

    return list(
        db.scalars(statement).all()
    )

def get_low_stock_products(
    db: Session,
):
    statement = (
        select(Product)
        .where(
            Product.stock
            <= Product.low_stock_threshold
        )
        .order_by(Product.stock.asc())
    )

    return list(
        db.scalars(statement).all()
    )