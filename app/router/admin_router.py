from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.model.user import User
from app.schemas.user_login import LoginResponse, LoginUser
from app.schemas.user_schema import CreateUser,UserResponse
from app.services.admin_service import admin_login_service, create_Admin_service
from app.session import get_session

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
)
def create_admin(
    user: CreateUser,
    session: Session = Depends(get_session),
):
    return  create_Admin_service(user, session)


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login_admin(
    data: LoginUser,
    session: Session = Depends(get_session),

):
    return admin_login_service(data, session)

