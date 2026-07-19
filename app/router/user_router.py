from fastapi import APIRouter, Depends
from sqlmodel import Session


from app.schemas.forgot_password import ForgotPasswordRequest, ForgotPasswordResponse
from app.schemas.reset_password import ResetPasswordRequest, ResetPasswordResponse
from app.schemas.user_login import LoginResponse, LoginUser
from app.schemas.user_schema import CreateUser, UserDto, UserResponse
from app.services.login_user import forgot_password_service, login_user, reset_password_service
from app.services.user_service import create_user, get_users
from app.session import get_session

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
)
def create_user_endpoint(
    user: CreateUser,
    session: Session = Depends(get_session),
):
    return create_user(user, session)


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    data: LoginUser,
    session: Session = Depends(get_session),
):
    return login_user(data, session)


@router.get(
    "/",
    response_model=list[UserDto],
)
def get_all_users(
    session: Session = Depends(get_session),
):
    return get_users(session)



@router.post(
    "/forgot-password",
    response_model=ForgotPasswordResponse,
)
async def forgot_password(
    data: ForgotPasswordRequest,
    session: Session = Depends(get_session),
):
    return await forgot_password_service(data, session)


@router.post(
    "/reset-password",
    response_model=ResetPasswordResponse,
)
def reset_password(
    data: ResetPasswordRequest,
    session: Session = Depends(get_session),
):
    return reset_password_service(data, session)