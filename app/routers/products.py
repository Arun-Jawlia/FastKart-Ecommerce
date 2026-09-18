from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.database.database import get_db
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    ProductListResponse
)
from app.services import category_service
from app.services import product_service, cache_service
from app.core.cache_keys import product_cache_key

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


@router.get('', response_model=ProductListResponse)
def get_products(
        page :int = Query(
        default = 1,
        ge = 1
    ),
    limit: int = Query(
        default = 20,
        ge = 1,
        le = 100
    ),
    search: str | None = None,
    category_id : int | None = Query(
        default= None,
        gt = 0
    ),
    min_price: int | None = Query(
        default = None,
        gt = 0
    ),
    max_price: int | None = Query(
        default = None,
        gt = 0
    ),
    sort_by: str = Query(
        default= "id",
        pattern = "^(id|name|price|stock)$"
    ),
    sort_order: str = Query(
        default = 'asc',
        pattern = "^(asc|desc)$"
    ),
    db: Session = Depends(get_db)):
    return product_service.get_products(
        db=db, 
        page = page, 
        limit=limit, 
        search = search, 
        category_id = category_id, 
        min_price = min_price, 
        max_price = max_price,
        sort_by = sort_by,
        sort_order = sort_order
        )


@router.get('/{product_id}', response_model=ProductResponse)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
):
    cache_key = product_cache_key(product_id)
    
    cached_product = cache_service.get_cache(cache_key)

    if cached_product:
        print("cache hit")
        return cached_product
    
    product = product_service.get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )
    product_data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "stock": product.stock,
        "category_id": product.category_id,
        "low_stock_threshold": product.low_stock_threshold,
    }

    cache_service.set_cache(
        cache_key,
        product_data,
        expire=300,
    )

    return product_data

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    product = product_service.get_product_by_id(db, product_id)
    print("Product avaialbel", type(product))
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
    
    updated_product = product_service.update_product(
        db,
        product,
        product_data
    )

    # invalidate cache
    cache_service.delete_cache(product_cache_key(product_id))
        
    return updated_product


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