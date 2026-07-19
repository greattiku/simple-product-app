from datetime import timedelta

from fastapi import HTTPException
from jose import jwt, JWTError
from sqlmodel import Session, select
from app.core.email import send_reset_email
from app.core.security import create_access_token, hash_password, verify_password
from app.model.user import User
from app.schemas.forgot_password import ForgotPasswordRequest, ForgotPasswordResponse
from app.schemas.reset_password import ResetPasswordRequest, ResetPasswordResponse
from app.schemas.user_login import LoginResponse, LoginUser
from app.schemas.user_schema import UserDto
from app.core.env import (
    AUTH_SECRET_KEY,
    ALGORITHM,
)

def login_user(login_data: LoginUser, session:Session):
    statement = select(User).where(
        User.email == login_data.email
    )
    user = session.exec(statement).first()
    print(f"password====={user.password}")
    if not user:
        raise HTTPException(
            status_code = 401,
            detail= "Invalid email or password",
        )
    
    if not verify_password(
        login_data.password,
        user.password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )
    
    access_token = create_access_token(
    {
        "sub": user.email,
        "user_id": user.id,
        "role": user.role.value,
    }
)
    
    return LoginResponse(
        message="Login successful",
        user=UserDto.model_validate(user),
        access_token=access_token,
    )



async def forgot_password_service(data: ForgotPasswordRequest, session: Session):
    user = session.exec(
        select(User).where(User.email == data.email)
    ).first()

    if not user:
        return ForgotPasswordResponse(
            message="If an account with that email exists, a password reset link has been sent."
        )

    reset_token = create_access_token(
        {
            "sub": user.email,
            "purpose": "password_reset",
        },
        expires_delta=timedelta(minutes=15),
    )

    await send_reset_email(
        user.email,
        reset_token,
    )
    return ForgotPasswordResponse(
        message="If an account with that email exists, a password reset link has been sent."
    )


def reset_password_service(data: ResetPasswordRequest, session: Session):
    try:
        payload = jwt.decode(
            data.token,
            AUTH_SECRET_KEY,
            algorithms=[ALGORITHM],
        )

    except JWTError:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired token",
        )

    if payload.get("purpose") != "password_reset":
        raise HTTPException(
            status_code=400,
            detail="Invalid token",
        )

    email = payload["sub"]

    user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    user.password = hash_password(data.new_password)

    session.add(user)
    session.commit()

    return ResetPasswordResponse(
        message="Password reset successful."
    )