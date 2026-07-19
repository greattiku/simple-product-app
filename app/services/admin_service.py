
from fastapi import HTTPException
from sqlmodel import Session, select
from app.model.user import User, UserRole
from app.schemas.user_schema import CreateUser, UserDto, UserResponse
from app.core.security import create_access_token, hash_password, verify_password
from app.schemas.user_login import LoginResponse, LoginUser



def create_Admin_service(create_user:CreateUser, session: Session):
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
            role=UserRole.ADMIN,
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



def admin_login_service(login_data: LoginUser, session:Session):
    statement = select(User).where(
        User.email == login_data.email
    )

    user = session.exec(statement).first()
    if not user:
        raise HTTPException(
            status_code = 401,
            detail= "Invalid email or password",
        )

    if user.role != UserRole.ADMIN:
            raise HTTPException(
            status_code=403,
            detail="Only admins can login here.",
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
