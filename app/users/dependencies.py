from datetime import datetime

from fastapi import Request, HTTPException, Depends, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.sql.functions import current_user

from app.config import settings
from app.database import get_async_session
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token

async def get_current_user(token:str = Depends(get_token), session: AsyncSession = Depends(get_async_session)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    expire: str = payload.get("exp")
    if not expire or datetime.utcfromtimestamp(int(expire)) < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token expired")
    user_id: str = payload.get("sub")
    if (not user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await UsersDAO.find_by_id(session, int(user_id))
    if (not user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user