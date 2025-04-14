from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.bookings.models import Bookings

router = APIRouter(prefix="/bookings",
                   tags=["Bookings"])

@router.get("")
async def get_bookings(session: AsyncSession = Depends(get_async_session)):
    pass
    # stmt = select(Bookings)
    # result = await session.execute(stmt)
    # return result.scalars().all()