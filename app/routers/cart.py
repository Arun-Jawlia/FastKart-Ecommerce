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

