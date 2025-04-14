from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.dao import BookingDAO
from app.database import get_async_session
router = APIRouter(prefix="/bookings",
                   tags=["Bookings"])


@router.get("")
async def get_bookings(session: AsyncSession = Depends(get_async_session)):
    return await BookingDAO.find_one_or_none(session, room_id = 3)
