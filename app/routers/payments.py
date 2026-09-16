#pylint: disable = all
from fastapi import APIRouter, HTTPException, status, Depends, Header
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
    PaymentVerify
)
from app.services import payment_service, payment_provider

router = APIRouter(
    prefix='/payments',
    tags = ['Payments']
)

@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(
    data: PaymentCreate,
    idempotency_key: str = Header(
        ..., 
        alias ='Idempotency-key'
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    payment, error = payment_service.create_payment(
        db= db,
        user_id = current_user.id,
        order_id= data.order_id,
        idempotency_key=idempotency_key
    )

    if error == 'ORDER_NOT_FOUND':
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail='Order Not Found'
        )

    if error == 'ORDER_CANCELLED':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot pay for cancelled order'
        )

    if error =='PAYMENT_EXISTS':
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "Cannot pay for cancelled order"
        )  
    
    if error == "ORDER_CANCELLED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot pay for cancelled order",
        )

    if error == "PAYMENT_EXISTS":
        return payment

    return payment    


@router.post(
    "/{payment_id}/verify",
    response_model=PaymentResponse,
)
def verify_payment(
    payment_id: int,
    data: PaymentVerify,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    payment, error = payment_service.verify_payment(
        db=db,
        user_id=current_user.id,
        payment_id=payment_id,
        provider_payment_id=data.provider_payment_id,
    )

    if error == "PAYMENT_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    if error == "INVALID_PAYMENT":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payment verification",
        )

    return payment

# @router.get(
#     "/generate/payment-provider-id",
# )
