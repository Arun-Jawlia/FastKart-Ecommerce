from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import (
    create_access_token, verify_password
)
from app.database.database import get_db
from app.schemas.auth import LoginRequest, TokenRequest
from app.services import user_service
from app.schemas.user import UserCreate, UserResponse
from app.services import rate_limit_service
from app.core.cache_keys import rate_limit_cache_key

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

# @router.post('/login', response_model=TokenRequest)
# def login(login_data: LoginRequest, db: Session = Depends(get_db)):
#     user = user_service.get_user_by_email(db, login_data.email)

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail='Invalid email or password'
#         )
    
#     if not verify_password(
#         login_data.password,
#         user.password
#     ):
#         raise HTTPException(
#             status_code= status.HTTP_401_UNAUTHORIZED,
#             detail='Invalid email or password'
#         )

#     access_token = create_access_token(user.id)

#     return {
#         'access_token': access_token,
#         "token_type": 'bearer'
#     }

@router.post("/login")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    client_ip = request.client.host
    rate_limit_key = rate_limit_cache_key(client_ip)

    allowed = rate_limit_service.check_rate_limit(
        key=rate_limit_key,
        limit=5,
        window=60
    )
    if not allowed:
        raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Too many login attempts. Try again later.",
        )
    user = user_service.get_user_by_email(db, form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



@router.post('/register', response_model = UserResponse, status_code=status.HTTP_201_CREATED,)
def regsiter(user_data: UserCreate, db: Session= Depends(get_db)):
    existing_user = user_service.get_user_by_email(db, user_data.email)

    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail='Email already registered'
        )

    return user_service.create_user(db, user_data)