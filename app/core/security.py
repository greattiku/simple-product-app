
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from jose import jwt
from pwdlib import PasswordHash
from app.core.env import (
    AUTH_SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
load_dotenv()


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )

def create_access_token(data: dict,expires_delta: timedelta | None = None):
    payload = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=5)
    )

    payload.update({"exp": expire})

    return jwt.encode(
    claims=payload,
    key=AUTH_SECRET_KEY,
    algorithm=ALGORITHM,
)