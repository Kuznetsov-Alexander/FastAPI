from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing.pickleable import User

from app.database import get_async_session
from app.users.auth import get_password_hash
from app.users.dao import UsersDAO
from app.users.schemas import SUserRegister

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/register")
async def register_user(user_data: SUserRegister, session: AsyncSession = Depends(get_async_session)):
    existing_user = await UsersDAO.find_one_or_none(session, email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500)
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(session, email=user_data.email, hashed_password=hashed_password)