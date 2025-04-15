from http.client import HTTPException

from alembic.util import status
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.users.auth import get_password_hash, verify_password, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.schemas import SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/register")
async def register_user(user_data: SUserAuth, session: AsyncSession = Depends(get_async_session)):
    existing_user = await UsersDAO.find_one_or_none(session, email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500)
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(session, email=user_data.email, hashed_password=hashed_password)

@router.post("/login")
async def login_user(response: Response ,user_data: SUserAuth, session: AsyncSession = Depends(get_async_session)):
    user = await authenticate_user(user_data.email, user_data.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token