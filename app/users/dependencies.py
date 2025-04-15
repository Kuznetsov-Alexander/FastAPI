from datetime import datetime

from fastapi import Request, Depends
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession


from app.config import settings
from app.database import get_async_session
from app.exceptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatException, \
    UserIsNotPresentException
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token:str = Depends(get_token), session: AsyncSession = Depends(get_async_session)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if not expire or datetime.utcfromtimestamp(int(expire)) < datetime.utcnow():
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if (not user_id):
        raise UserIsNotPresentException
    user = await UsersDAO.find_by_id(session, int(user_id))
    if (not user):
        raise UserIsNotPresentException

    return user