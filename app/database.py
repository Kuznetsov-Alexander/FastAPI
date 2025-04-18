from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_session
from sqlalchemy.orm import sessionmaker, DeclarativeBase


from app.config import settings


engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
