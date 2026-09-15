from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from decimal import Decimal
from app.services import inventory_services

def create_order_from_cart(
        db: Session,
        user_id: int,
        address: dict
): 
    
    cart = db.scalar(
        select(Cart).where(
            Cart.user_id == user_id
        )
    )

    if cart is None:
        return None, 'CART_NOT_FOUND'

    if not cart.items:
        return None, 'CART_EMPTY'

    # Calculate Stock First
    for cart_item in cart.items:
        product = cart_item.product

        if cart_item.quantity > product.stock:
            return None, (
                f"INSUFFICENT_STOCK:{product.id}"
            )
    
    # Calculate total
    subtotal = Decimal("0.00")

    for cart_item in cart.items:
        product = cart_item.product

        item_subtotal =  product.price * cart_item.quantity

        subtotal += item_subtotal

    total = subtotal

    # Create Order

    order = Order(
        user_id = user_id,
        status = "PENDING",
        subtotal = subtotal,
        total = total,
        shipping_full_name=address.full_name,
        shipping_phone=address.phone,
        shipping_address_line=address.address_line,
        shipping_city=address.city,
        shipping_state=address.state,
        shipping_postal_code=address.postal_code,
        shipping_country=address.country,
    )

    db.add(order)
    db.flush()

    # Create Order Items
    for cart_item in cart.items:

        product = cart_item.product

        item_subtotal = product.price * cart_item.quantity

        order_item = OrderItem(
            order_id = order.id,
            product_id = product.id,
            product_name = product.name,
            quantity= cart_item.quantity,
            unit_price = product.price,
            subtotal = item_subtotal
        )

        db.add(order_item)

    # Deduct Stock
    # for cart_item in cart.items:
    #     cart_item.product.stock -= cart_item.quantity

    for cart_item in cart.items:
        success = inventory_services.record_sale(
            db = db,
            product = cart_item.product,
            quantity = cart_item.quantity
        )

        if not success:
            db.rollback()
            return None, (
                f"INSUFFICIENT_STOCK:{cart_item.product.id}"
            )

    # clear cart
    for cart_item in cart.items:
        db.delete(cart_item)
    
    db.commit()
    db.refresh(order)

    return order, None


# Get All Orders
def get_user_orders(
    db: Session,
    user_id: int,
):
    statement = (
        select(Order)
        .where(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
    )

    return list(db.scalars(statement).all())


# Get Specific Order
def get_user_orders(
    db: Session,
    user_id: int,
):
    statement = (
        select(Order)
        .where(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
    )

    return list(db.scalars(statement).all())

def get_user_order(
    db: Session,
    user_id: int,
    order_id: int,
):
    statement = select(Order).where(
        Order.id == order_id,
        Order.user_id == user_id,
    )

    return db.scalar(statement)

def get_all_orders(
    db: Session,
):
    statement = (
        select(Order)
        .order_by(Order.created_at.desc())
    )

    return list(db.scalars(statement).all())

def update_order_status(
    db: Session,
    order: Order,
    status: str,
):
    order.status = status

    db.commit()
    db.refresh(order)

    return order
