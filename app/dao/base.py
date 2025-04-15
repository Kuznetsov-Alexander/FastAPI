from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, session: AsyncSession, model_id: int):
        query = select(cls.model).filter_by(id = model_id)
        result = await session.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filters_by):
        query = select(cls.model).filter_by(**filters_by)
        result = await session.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def find_all(cls, session: AsyncSession, **filters_by):
        query = select(cls.model).filter_by(**filters_by)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def add(cls, session: AsyncSession, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()