from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from settings.config import ASYNC_DB_URL

# Configure and connect to the database.
engine: AsyncEngine = create_async_engine(ASYNC_DB_URL)

SQLSession: async_sessionmaker[AsyncSession] = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(schema='public')


async def create_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
