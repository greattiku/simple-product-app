# app/core/auth.py

import os

from dotenv import load_dotenv
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.session import get_session
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from app.core.env import (
    AUTH_SECRET_KEY,
    ALGORITHM,
)
from app.model.user import User, UserRole

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            AUTH_SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user


def get_current_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )

    return current_user