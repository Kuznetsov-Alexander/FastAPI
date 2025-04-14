from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO


class BookingDAO(BaseDAO):
    model = Bookings
