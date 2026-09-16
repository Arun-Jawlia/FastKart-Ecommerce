import secrets
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.payment import Payment


def generate_transaction_reference():
    return(
        "PAY-" + secrets.token_hex(8).upper()
    )

def create_payment(
    db: Session,
    user_id: int,
    order_id: int,
    idempotency_key: str
):
    existing_payment = db.scalar(
        select(Payment)
        .where(
            Payment.idempotency_key == idempotency_key
        )
    )

    if existing_payment:
        return existing_payment, None

    order = db.scalar(
        select(Order)
        .where(
            Order.id == order_id,
            Order.user_id == user_id
        )
    )   

    if order is None:
        return None, "ORDER_NOT_FOUND"


    if order.status == 'CANCELLED':
        return None, 'ORDER_CANCELLED'
    
    existing_order_payment = db.scalar(
        select(Payment)
        .where(
            Payment.order_id == order.id
        )
    )

    if existing_order_payment:
        return existing_order_payment, "PAYMENT_EXISTS"

    payment = Payment(
        order_id = order.id,
        amount = order.total,
        currency="INR",
        status= 'PENDING',
        provider = 'MOCK',
        transaction_reference = generate_transaction_reference(),
        idempotency_key = idempotency_key
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment, None

    
def verify_payment(
    db: Session,
    user_id: int,
    payment_id: int,
    provider_payment_id: str,
):
    payment = db.scalar(
        select(Payment)
        .join(Order)
        .where(
            Payment.id == payment_id,
            Order.user_id == user_id,
        )
    )

    if payment is None:
        return None, "PAYMENT_NOT_FOUND"

    if payment.status == "SUCCESS":
        return payment, None
    
    if payment.provider_payment_id:
        if (
            payment.provider_payment_id
            != provider_payment_id
        ):
            return None, "INVALID_PAYMENT"

        return payment, None

    payment.provider_payment_id = (
        provider_payment_id
    )

    payment.status = "SUCCESS"

    payment.order.status = "CONFIRMED"

    db.commit()
    db.refresh(payment)

    return payment, None