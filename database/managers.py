from datetime import datetime
from decimal import Decimal
from typing import Any, Sequence

from sqlalchemy import Row, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.decorators import database_transaction
from database.models import StopVolume, Ticker, Trend
from settings.constants import LONG, STANDART_STOP
from tg_bot.send_message import send_message


class RowManager:
    """A manager class for performing database operations on rows."""
    @staticmethod
    @database_transaction
    async def add_row(sess_db: AsyncSession, table: Any, data: dict[str, Any]) -> None:
        """Create a new row in the table."""
        sess_db.add(table(**data))

    @staticmethod
    @database_transaction
    async def add_all_rows(sess_db: AsyncSession, list_rows: list[Any]) -> None:
        """Create new rows in the table."""
        sess_db.add_all(list_rows)

    @staticmethod
    @database_transaction
    async def delete_row_by_id(sess_db: AsyncSession, table: Any, id: int) -> None:
        """Delete a row in the table by ID."""
        await sess_db.delete(await sess_db.get(table, id))

    @staticmethod
    @database_transaction
    async def get_all_rows(sess_db: AsyncSession, table: Any) -> list[dict[str, Any]]:
        """Query all table rows."""
        query = (await sess_db.execute(select(table))).scalars().all()
        return [row.__dict__ for row in query]

    @staticmethod
    @database_transaction
    async def get_row_by_id(sess_db: AsyncSession, table: Any, id: int) -> Any:
        """Request a row by id."""
        return await sess_db.get(table, id)

    @staticmethod
    @database_transaction
    async def get_limit_row(
        sess_db: AsyncSession, table: Any, ticker: str, trend: str, limit: int
    ) -> Sequence[Any]:
        """Request a certain number of table rows."""
        return (
            await sess_db.execute(
                select(table)
                .where(table.ticker == ticker, table.trend == trend)
                .order_by(table.level if trend == LONG else table.level.desc())
                .limit(limit=limit)
            )
        ).scalars().all()

    @classmethod
    async def transferring_row(
        cls, table: Any, id: int, ticker: str, level: Decimal, trend: str,
        median_price: Decimal | None, update_median_price: datetime | None,
    ) -> None:
        """Transfer a row from one table to another."""
        await cls.add_row(
            table,
            {
                'ticker': ticker,
                'level': level,
                'trend': trend,
                'median_price': median_price,
                'update_median_price': update_median_price
            }
        )
        await cls.delete_row_by_id(Ticker, id)


class ConfigurationManager:
    """A manager class for changing system configuration parameters."""
    @staticmethod
    @database_transaction
    async def change_trend(sess_db: AsyncSession, trend: str) -> None:
        """Change the direction of the trend."""
        if (row := await sess_db.get(Trend, 1)) is not None:
            setattr(row, 'trend', trend)
            return
        sess_db.add(Trend(trend=trend))

    @staticmethod
    @database_transaction
    async def change_stop(sess_db: AsyncSession, volume: Decimal) -> None:
        """Change in the value of the stop."""
        if (row := await sess_db.get(StopVolume, 1)) is not None:
            setattr(row, 'usdt_volume', volume)
            return
        sess_db.add(StopVolume(usdt_volume=volume))


class TickerManager:
    """A manager class for query ticker information."""
    @staticmethod
    @database_transaction
    async def get_current_level(
        sess_db: AsyncSession, ticker: str, trend: str
    ) -> Row[tuple[int, Decimal, Decimal, datetime]] | None:
        """Request a level to check the compliance of the parameters of the opening of the transaction."""
        level = (
                select(
                    func.min(Ticker.level)
                    if trend == LONG else
                    func.max(Ticker.level)
                )
                .where(
                    Ticker.ticker == ticker,
                    Ticker.trend == trend
                )
                .scalar_subquery()
            )
        return (
            await sess_db.execute(
                select(Ticker.id, Ticker.level, Ticker.median_price, Ticker.update_median_price)
                .where(
                    Ticker.ticker == ticker,
                    Ticker.level == level
                )
            )
        ).fetchone()

    @staticmethod
    @database_transaction
    async def get_tickers_by_trend(sess_db: AsyncSession, trend: str) -> Sequence[str]:
        """Request all tickers by the trend."""
        return (
            await sess_db.execute(
                select(Ticker.ticker)
                .distinct()
                .where(Ticker.trend == trend)
            )
        ).scalars().all()

    @staticmethod
    @database_transaction
    async def get_level_by_trend(sess_db: AsyncSession, ticker: str, trend: str) -> set[Decimal]:
        """Request ticker levels for the selected trend."""
        return set(
            (
                await sess_db.execute(
                    select(Ticker.level)
                    .where(
                        Ticker.ticker == ticker, Ticker.trend == trend
                    )
                )
            )
            .scalars().all()
        )

    @staticmethod
    @database_transaction
    async def set_median_price(sess_db: AsyncSession, id: int, median_price: Decimal) -> None:
        """Update the average price and the update time for a specific ticker in the database."""
        if (row := await sess_db.get(Ticker, id)) is not None:
            setattr(row, 'median_price', median_price)
            setattr(row, 'update_median_price', datetime.now())


async def set_standart_stop():
    """If the stop is not defined, then set the standard one."""
    if await RowManager.get_row_by_id(StopVolume, 1) is None:
        await ConfigurationManager.change_stop(STANDART_STOP)
        await send_message(f'Added standard stop volume: {STANDART_STOP} USDT')
