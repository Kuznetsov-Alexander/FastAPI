from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert, func, and_, or_
from datetime import date
from app.bookings.models import Bookings

from app.dao.base import BaseDAO
from app.database import engine, async_session_maker
from app.hotels.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings


    @classmethod
    async def add(cls, session: AsyncSession, user_id: int, room_id: int, date_from: date, date_to: date):

        # '''
        # WITH booked_rooms AS(
        # SELECT * FROM bookings
        # where room_id = 1 and
        # (date_from >= '2033-05-15' and date_from <= '2033-06-20') or
        # (date_from <= '2033-05-15' and date_to > '2033-05-15')
        # )
        #
        # select rooms.quantity - COUNT(booked_rooms.room_id) from rooms
        # LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        # WHERE rooms.id = 1
        # GROUP BY rooms.quantity, booked_rooms.room_id
        # '''
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == 1,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                            ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        ),
                    )
                )
            ).cte("booked_rooms")

            get_rooms_left = select(
                                Rooms.quantity - func.count(booked_rooms.c.room_id).label("rooms_left")
                                ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Rooms.id == 1).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )

            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price:int = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Bookings)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()

            else: return None

