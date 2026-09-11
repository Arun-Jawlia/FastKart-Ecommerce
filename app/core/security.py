from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from app.core.config import settings

pasword_hash = PasswordHash.recommended()

def hash_password(password: str)->str:
    return pasword_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> str:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(user_id: int)->str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        'sub': str(user_id),
        "exp": expires
    }

    return jwt.encode(
        payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )