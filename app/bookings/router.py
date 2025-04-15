from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.dao import BookingDAO
from app.database import get_async_session
from app.bookings.schemas import SBooking
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix="/bookings",
                   tags=["Bookings"])


@router.get("")
async def get_bookings(
    user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> list[SBooking]:
    return await BookingDAO.find_all(session, user_id=user.id)
