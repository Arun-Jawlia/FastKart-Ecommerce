from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import (
    create_access_token, verify_password
)
from app.database.database import get_db
from app.schemas.auth import LoginRequest, TokenRequest
from app.services import user_service
from app.schemas.user import UserCreate, UserResponse

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
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
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