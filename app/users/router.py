from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordExeption
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/register")
async def register_user(user_data: SUserAuth, session: AsyncSession = Depends(get_async_session)):
    existing_user = await UsersDAO.find_one_or_none(session, email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(session, email=user_data.email, hashed_password=hashed_password)

@router.post("/login")
async def login_user(response: Response ,user_data: SUserAuth, session: AsyncSession = Depends(get_async_session)):
    user = await authenticate_user(user_data.email, user_data.password, session)
    if not user:
        raise IncorrectEmailOrPasswordExeption
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")

@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user