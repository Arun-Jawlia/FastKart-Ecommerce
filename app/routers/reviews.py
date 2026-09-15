from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.review import (
    ReviewCreate,
    ReviewResponse,
    ReviewUpdate
)
from app.database.database import get_db

from app.services import review_service

router = APIRouter(
    prefix = '/reviews',
    tags = ['Reviews']
)


@router.post("/products/{product_id}", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    product_id: int,
    data: ReviewCreate,
    current_user : User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    review, error = review_service.create_review(
        db= db,
        user_id = current_user.id,
        product_id = product_id,
        data = data
    )

    if error == "NOT_PURCHASED":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            details ='You can review only products you purchased'
        )
    if error == "ALREADY_REVIEWED":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail ='You have already reviewed this product'
        )
    
    return review


@router.get(
    "/products/{product_id}",
    response_model=list[ReviewResponse],
)
def get_product_reviews(
    product_id: int,
    db: Session = Depends(get_db),
):
    return review_service.get_product_reviews(
        db,
        product_id,
    )

@router.put(
    "/{review_id}",
    response_model=ReviewResponse,
)
def update_review(
    review_id: int,
    data: ReviewUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    review = review_service.update_review(
        db=db,
        user_id=current_user.id,
        review_id=review_id,
        data=data,
    )

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    return review

@router.delete(
    "/{review_id}",
)
def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deleted = review_service.delete_review(
        db=db,
        user_id=current_user.id,
        review_id=review_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    return {
        "message": "Review deleted",
    }