from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from app.services import user_service
from app.database.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:

    credentails_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = 'Could not validate credentials',
        headers = {
            "WWW-Authenticate": "Bearer"
        }
    )

    try:
        payload = jwt.decode(
            token, 
            settings.jwt_secret_key,
            algorithms=settings.jwt_algorithm
        )

        user_id = payload.get('sub')

        if user_id is None:
            raise credentails_exception

    except InvalidTokenError:
        raise credentails_exception

    user = user_service.get_user_by_id(db, int(user_id))

    if user is None:
        raise credentails_exception
        
    return user


def require_admin(current_user : User = Depends(get_current_user))->User:
    if current_user.role != 'ADMIN':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Admin access required'
        )
    
    return current_user