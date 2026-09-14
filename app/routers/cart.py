from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.cart import (
    CartItemAdd,
    CartItemResponse,
    CartItemUpdate,
    CartResponse
)
from app.services import cart_service

router = APIRouter(
    prefix='/cart',
    tags=['Cart']
)

@router.get('', response_model=CartResponse)
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    return cart_service.get_cart(
        db=db,
        user_id=current_user.id
    )

@router.post('/items', status_code = status.HTTP_201_CREATED)
def add_cart_item(
    data: CartItemAdd,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item, error = cart_service.add_item(
        db = db,
        user_id = current_user.id,
        product_id=data.product_id,
        quantity = data.quantity
    )

    if error == 'PRODUCT_NOT_FOUND':
        raise HTTPException(
            status_code =status.HTTP_404_NOT_FOUND,
            detail = 'Product not found'
        )
    
    if error == 'INSUFFICENT_STOCK':
        raise HTTPException(
            status_code =status.HTTP_404_NOT_FOUND,
            detail = 'Insufficient product stokc'
        )
    
    return {
        "message": "Product added to cart",
        "item_id": item.id
    }

@router.put(
    "/items/{item_id}",
)
def update_cart_item(
    item_id: int,
    data: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item, error = cart_service.update_item(
        db=db,
        user_id=current_user.id,
        item_id=item_id,
        quantity=data.quantity,
    )

    if error == "ITEM_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found",
        )

    if error == "INSUFFICIENT_STOCK":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient product stock",
        )

    return {
        "message": "Cart item updated",
    }

@router.delete(
    "/items/{item_id}",
)
def remove_cart_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    removed = cart_service.remove_item(
        db=db,
        user_id=current_user.id,
        item_id=item_id,
    )

    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found",
        )

    return {
        "message": "Cart item removed",
    }

@router.delete("")
def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart_service.clear_cart(
        db=db,
        user_id=current_user.id,
    )

    return {
        "message": "Cart cleared",
    }