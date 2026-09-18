from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.dependencies import (
    get_current_user,
    require_admin
)
from app.database.database import get_db
from app.models.user import User
from app.schemas.order import (
    OrderResponse,
    OrderStatusUpdate,
    CheckoutRequest
)
from app.models.order import Order
from app.services import order_service, address_service, email_service

router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)

@router.post('/checkout', response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def checkout(
    data: CheckoutRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
): 

    address = address_service.get_address(
        db=db,
        user_id=current_user.id,
        address_id=data.address_id,
        )

    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )
    order, error = order_service.create_order_from_cart(db=db, user_id=current_user.id, address=address)

    if error == 'CART_NOT_FOUND':
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = 'Cart not found'
        )
    if error == "CART_EMPTY":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty",
        )

    if error and error.startswith("INSUFFICIENT_STOCK"):
        product_id = error.split(":")[1]

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock for product {product_id}",
        )
    background_tasks.add_task(
        email_service.send_order_confirmation_email,
        current_user.email,
            order.id,
    )

    return order    

@router.get('', response_model=list[OrderResponse])
def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    return order_service.get_user_orders(
        db= db,
        user_id = current_user.id
    )
@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_my_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = order_service.get_user_order(
        db=db,
        user_id=current_user.id,
        order_id=order_id,
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return order

@router.get(
    "/admin/all",
    response_model=list[OrderResponse],
)
def get_all_orders(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return order_service.get_all_orders(db)

@router.patch(
    "/admin/{order_id}/status",
    response_model=OrderResponse,
)
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    allowed_statuses = {
        "PENDING",
        "CONFIRMED",
        "SHIPPED",
        "DELIVERED",
        "CANCELLED",
    }

    if data.status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order status",
        )

    order = db.get(Order, order_id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return order_service.update_order_status(
        db=db,
        order=order,
        status=data.status,
    )