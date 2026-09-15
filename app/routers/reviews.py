from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.review import (
    ReviewCreate,
    ReviewResponse,
    ReviewUpdate
)

from app.services import review_service

router = APIRouter(
    prefix = '/reviews',
    tags = ['Reviews']
)
