from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import (
    get_current_user,
    require_admin
)
from app.database.database import get_db
from app.models.user import User
from app.schemas.order import (
    OrderResponse,
    OrderStatusUpdate
)
from app.services import order_service

router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)

