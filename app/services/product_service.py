from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductUpdate
)
from decimal import Decimal
from app.services import cache_service


def create_product(
        db: Session, 
        product_data: ProductCreate
    ) -> Product:
    product = Product(
        name = product_data.name,
        description = product_data.description,
        price = product_data.price,
        stock= product_data.stock,
        category_id = product_data.category_id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product

def get_products(
    db: Session,
    page: int,
    limit: int,
    search: str | None = None,
    category_id: int | None = None,
    min_price : int | None = None,
    max_price : int | None = None,
    sort_by: str = 'id',
    sort_order: str = 'asc'
):
    statement = select(Product)
    if search:
        search_term = f"%{search}%"

        statement = statement.where(
            Product.name.ilike(search_term)
        )

    if category_id is not None:
        statement = statement.where(
            Product.category_id == category_id
        )

    if min_price is not None:
        statement = statement.where(
            Product.price >= min_price
        )

    if max_price is not None:
        statement = statement.where(
            Product.price <= max_price
        )    
    
    # Count filtered results
    count_statement = select(
        func.count()
    ).select_from(
        statement.subquery()
    )

    total = db.scalar(
        count_statement
    ) or 0    
    
    allowed_sort_fields = {
    "id": Product.id,
    "name": Product.name,
    "price": Product.price,
    "stock": Product.stock,
    }
    sort_column = allowed_sort_fields.get(sort_by)

    if sort_column is None:
        raise ValueError(
            "Invalid sort field"
        )
    if sort_order == "desc":
        statement = statement.order_by(
            sort_column.desc()
        )
    else:
        statement = statement.order_by(
            sort_column.asc()
        )
    
    offset = (page - 1) * limit
    
    products = list(
        db.scalars(statement).all()
    )
    statement = statement.offset(
        offset
    ).limit(
        limit
    )

    products = list(
        db.scalars(statement).all()
    )

    total_pages = (
        total + limit - 1
    ) // limit

    return {
        "items": products,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
    }

def get_product_by_id(
        db: Session,
        product_id: int
) -> Product | None:
    
    cache_key = f"product:{product_id}"
    
    cached_product = cache_service.get_cache(cache_key)

    if cached_product:
        print("cache hit")
        return cached_product

    product = db.get(Product, product_id)

    if product is None:
        return None
    
    product_data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "stock": product.stock,
        "category_id": product.category_id,
        "low_stock_threshold": (
            product.low_stock_threshold
        ),
    }

    cache_service.set_cache(
        cache_key,
        product_data,
        expire=300,
    )

    return product_data


def update_product(
        db: Session,
        product: Product,
        product_data: ProductUpdate
) -> Product | None:
    
    update_data = product_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(update_data, field, value)

    db.commit()
    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product: Product,
) -> None:

    db.delete(product)
    db.commit()


