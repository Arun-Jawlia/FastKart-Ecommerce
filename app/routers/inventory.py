from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import require_admin
from app.database.database import get_db
from app.models.user import User
from app.schemas.inventory import InventoryTransactionResponse, StockSet, StockUpdate
from app.services import inventory_service, cache_service
from app.core.cache_keys import product_cache_key


router = APIRouter(
    prefix='/inventory',
    tags=['Inventory']
)

@router.post('/products/{product_id}/restock')
def restock_product(
    product_id: int,
    data: StockUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    product, error = inventory_service.restock_product(
        db= db,
        product_id=product_id,
        quantity = data.quantity,
        reason = data.reason
    )

    if error == 'PRODUCT_NOT_FOUND':
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Product not found'
        )
    
        # invalidate cache
    cache_service.delete_cache(product_cache_key(product_id))

    
    return {
        "message": "Product Restocked",
        "product_id": product.id,
        "stock": product.stock
    }


@router.post(
    "/products/{product_id}/remove",
)
def remove_stock(
    product_id: int,
    data: StockUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    product, error = inventory_service.remove_stock(
        db=db,
        product_id=product_id,
        quantity=data.quantity,
        reason=data.reason,
    )

    if error == "PRODUCT_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    if error == "INSUFFICIENT_STOCK":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock",
        )

    return {
        "message": "Stock removed",
        "product_id": product.id,
        "stock": product.stock,
    }

@router.put(
    "/products/{product_id}",
)
def set_product_stock(
    product_id: int,
    data: StockSet,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    product, error = inventory_service.set_stock(
        db=db,
        product_id=product_id,
        quantity=data.quantity,
        reason=data.reason,
    )

    if error == "PRODUCT_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return {
        "message": "Stock updated",
        "product_id": product.id,
        "stock": product.stock,
    }

@router.get(
    "/products/{product_id}/history",
    response_model=list[InventoryTransactionResponse],
)
def get_inventory_history(
    product_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return inventory_service.get_inventory_history(
        db,
        product_id,
    )

@router.get(
    "/low-stock",
)
def get_low_stock_products(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    products = inventory_service.get_low_stock_products(
        db
    )

    return products