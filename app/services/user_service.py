

from fastapi import HTTPException
from sqlmodel import Session, select

from app.core.security import hash_password
from app.model.user import User, UserRole
from app.schemas.product_schema import ProductResponse
from app.schemas.user_schema import CreateUser, UserDto, UserResponse


def create_user(create_user:CreateUser, session: Session):
    existing_user = session.exec(
        select(User).where(User.email == create_user.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail= "User with that email already exists"
        )
    
    db_user = User(
         **create_user.model_dump(exclude={"password"}),
            role=UserRole.CUSTOMER,
            password=hash_password(create_user.password),
            is_active=False,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return UserResponse(
        message= "User created successfully",
        user=UserDto.model_validate(db_user)
    )


def get_users(session:Session):
    users = session.exec(select(User)).all()

    return [
        UserDto.model_validate(user)
        for user in users
    ]
