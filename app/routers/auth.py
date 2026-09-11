from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import (
    create_access_token, verify_password
)
from app.database.database import get_db
from app.schemas.auth import LoginRequest, TokenRequest
from app.services import user_services

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/login', response_model=TokenRequest)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = user_services.get_user_by_email(db, login_data.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password'
        )
    
    if not verify_password(
        login_data.password,
        user.password
    ):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password'
        )

    access_token = create_access_token(user.id)

    return {
        'access_token': access_token,
        "token_type": 'bearer'
    }

