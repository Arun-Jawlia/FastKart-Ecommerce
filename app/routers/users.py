#pylint: disable = all
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.user import (
    UserUpdate,
    UserResponse,
    UserCreate
)
from app.services import user_service

from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session= Depends(get_db)):
    existing_user = user_service.get_user_by_email(db, user_data.email)

    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail='Email already registered'
        )
    
    return user_service.create_user(
        db, user_data
    )

@router.get('', response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)

@router.get('/me', response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.get('/{user_id}', response_model=UserResponse)
def get_user_by_id(user_id: int, db:Session= Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    return user

@router.put('/{user_id}', response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate ,db:Session= Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    return user_service.update_user(
        db, user, user_data
    )

@router.delete('/{user_id}')
def delete_user(user_id: int, db:Session= Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    user_service.delete_user(db, user)

    return {
        'message':"User Deleted"
    }