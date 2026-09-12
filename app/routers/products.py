from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.database.database import get_db
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.services import category_service
from app.services import product_service


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

@router.post('', response_model= ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate, 
    db: Session = Depends(get_db),
    current_user : User = Depends(require_admin)
):

    category = category_service.get_category_by_id(
        db,
        product_data.category_id
    )

    if not category:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Category not found'
        )
    
    return product_service.create_product(db, product_data)


@router.get('', response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return product_service.get_products(db)


@router.get('/{product_id}', response_model=ProductResponse)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = product_service.get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    product = product_service.get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )

    if product_data.category_id is not None:
        category = category_service.get_category_by_id(db, product_data.category_id)

        if not category:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = 'Category not found'
            )
        
    return product_service.update_product(
        db,
        product,
        product_data
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    product = product_service.get_product_by_id(
        db,
        product_id,
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    product_service.delete_product(
        db,
        product,
    )