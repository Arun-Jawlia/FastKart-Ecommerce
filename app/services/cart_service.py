from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product


def get_or_create_cart(
    db: Session,
    user_id: int
)->Cart:

    statement = select(Cart).where(
        Cart.user_id == user_id
    )

    cart = db.scalar(statement)

    if cart:
        return cart
    
    cart = Cart(user_id = user_id)

    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def get_cart(
    db: Session,
    user_id: int
) -> Cart:

    cart = get_or_create_cart(db,user_id)

    items = []

    total = Decimal("0.00")

    for item in cart.items:
        subtotal = item.product.price * item.quantity

        items.append(
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_name": item.product.name,
                "price":item.product.price,
                "quantity": item.quantity,
                "subtotal": subtotal
            }
        )

        total += subtotal
    
    return {
        "id": cart.id,
        "items":items,
        "total":total
    }


def add_item(
        db: Session,
        user_id: int,
        product_id: int,
        quantity: int
):

    cart = get_or_create_cart(db, user_id)

    product = db.get(Product, product_id)

    if product is None:
        return None, "PRODUCT_NOT_FOUND"
    
    if quantity > product.stock:
        return None, "INSUFFICIENT_STOCK"
    
    statement = select(CartItem).where(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    )

    cart_item = db.scalar(statement)

    if cart_item:
        new_quantity= cart_item.quantity + quantity

        if new_quantity > product.stock:
            return None, "INSUFFICIENT_STOCK"

        cart_item.quantity = new_quantity
    
    else:
        cart_item = CartItem(
            cart_id = cart.id,
            product_id = product_id,
            quantity= quantity
        )


        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item, None


def update_item(
        db: Session,
        user_id: int,
        item_id: int,
        quantity: int
):

    cart = get_or_create_cart(db, user_id)

    cart_item = db.scalar(
        select(CartItem)
        .where(
            CartItem.id == item_id,
            CartItem.cart_id == cart.id
        )
    )

    if cart_item is None:
        return None, 'ITEM_NOT_FOUND'

    if quantity > cart_item.product.stock:
        return None, 'INSUFFICIENT_STOCK'
    
    cart_item.quantity = quantity

    db.commit()
    db.refresh(cart_item)
    return cart_item, None


def remove_item(
    db: Session,
    user_id: int,
    item_id: int,
):
    cart = get_or_create_cart(db, user_id)

    cart_item = db.scalar(
        select(CartItem)
        .where(
            CartItem.id == item_id,
            CartItem.cart_id == cart.id,
        )
    )

    if cart_item is None:
        return False

    db.delete(cart_item)
    db.commit()

    return True

def clear_cart(
    db: Session,
    user_id: int,
):
    cart = get_or_create_cart(db, user_id)

    for item in cart.items:
        db.delete(item)

    db.commit()