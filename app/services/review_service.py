from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.review import Review

def has_purchased_product(
        db: Session,
        user_id: int,
        product_id: int
): 
    statement = (
        select(OrderItem.id)
        .join(Order)
        .where(
            Order.user_id == user_id,
            OrderItem.product_id == product_id,
            Order.status != 'CANCELLED'
        )
        .limit(1)
    )

    return db.scalar(statement) is not None


def create_review(
    db: Session,
    user_id: int,
    product_id: int,
    data
):
    purchased = has_purchased_product(db, user_id, product_id)

    if not purchased:
        return None, 'NOT_PURCHASED'

    existing = db.scalar(
        select(Review)
        .where(
            Review.user_id == user_id,
            Review.product_id == product_id
        )
    )

    if existing:
        return None, 'ALREADY_REVIEWED'
    
    review = Review(
        user_id=user_id,
        product_id=product_id,
        rating=data.rating,
        comment=data.comment,
    )


    db.add(review)
    db.commit()
    db.refresh(review)

    return review, None


def get_product_reviews(
    db: Session,
    product_id: int
):
    statement = (
        select(Review)
        .where(
            Review.product_id == product_id
        )
        .order_by(
            Review.created_at.desc()
        )
    )

    return list(db.scalars(statement).all())

def get_user_review(
    db: Session,
    user_id: int,
    review_id: int,
):
    statement = select(Review).where(
        Review.id == review_id,
        Review.user_id == user_id,
    )

    return db.scalar(statement)


def update_review(
    db: Session,
    user_id: int,
    review_id: int,
    data,
):
    review = get_user_review(
        db,
        user_id,
        review_id,
    )

    if review is None:
        return None

    update_data = data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)

    return review

def delete_review(
    db: Session,
    user_id: int,
    review_id: int,
):
    review = get_user_review(
        db,
        user_id,
        review_id,
    )

    if review is None:
        return False

    db.delete(review)
    db.commit()

    return True