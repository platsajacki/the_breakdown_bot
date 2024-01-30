from decimal import Decimal
from typing import Any

from sqlalchemy import Row, func
from sqlalchemy.orm import Session

from database.db import engine
from database.models import Base, StopVolumeDB, TickerDB, TrendDB
from decorators import database_return, database_transaction
from settings import LONG
from tg_bot.send_message import send_message


class Manager:
    """Query database manager."""
    @staticmethod
    @database_transaction
    def add_to_table(sess_db: Session, table, data: dict[str, Any]) -> None:
        """Add records to the table."""
        sess_db.add(table(**data))

    @staticmethod
    @database_transaction
    def delete_row(sess_db: Session, table, id: int) -> None:
        """Delete records in the table."""
        sess_db.delete(sess_db.query(table).filter(table.id == id).one())

    @staticmethod
    @database_transaction
    def changing_trend(sess_db: Session, trend: str) -> None:
        """Change the direction of the trend."""
        row: Row | None = sess_db.query(TrendDB).get(1)
        if row is not None:
            row.trend = trend
        else:
            sess_db.add(TrendDB(trend=trend))

    @staticmethod
    @database_transaction
    def changing_stop(sess_db: Session, volume: Decimal) -> None:
        """Change in the value of the stop."""
        row: Row | None = sess_db.query(StopVolumeDB).get(1)
        if row is not None:
            row.usdt_volume = volume
        else:
            sess_db.add(StopVolumeDB(usdt_volume=volume))

    @staticmethod
    @database_return
    def get_all_rows(sess_db: Session, table) -> list[dict[str, Any]]:
        """Query all table rows."""
        return [q.__dict__ for q in sess_db.query(table).all()]

    @staticmethod
    @database_return
    def get_row_by_id(sess_db: Session, table, id: int) -> Any:
        """Request a row by id."""
        return sess_db.query(table).get(id)

    @staticmethod
    @database_return
    def get_limit_query(
        sess_db: Session, table, ticker: str, trend: str, limit: int
    ) -> list[dict[str, Any]]:
        """Request a certain number of table rows."""
        query: list[Any[Base]] = (
            sess_db.query(table)
            .filter(table.ticker == ticker, table.trend == trend)
            .order_by(table.level if trend == LONG else table.level.desc())
            .limit(limit=limit)
        ).all()
        return [q.__dict__ for q in query]

    @staticmethod
    @database_return
    def select_trend_tickers(sess_db: Session, trend: str) -> list[Row]:
        """Request all tickers by the trend."""
        return sess_db.query(TickerDB.ticker).distinct().filter(TickerDB.trend == trend).all()

    @staticmethod
    @database_return
    def get_current_level(sess_db: Session, ticker: str, trend: str) -> None | dict[str, int | Decimal]:
        """Request a level to check the compliance of the parameters of the opening of the transaction."""
        level: Row[tuple] | None = (
            sess_db.query(
                func.min(TickerDB.level)
                if trend == LONG else
                func.max(TickerDB.level)
            )
            .filter(
                TickerDB.ticker == ticker,
                TickerDB.trend == trend
            )
        ).one_or_none()
        return None if level is None else (
            sess_db.query(TickerDB.id, TickerDB.level)
            .filter(
                TickerDB.ticker == ticker,
                TickerDB.level == level[0]
            )
        ).one()._asdict()

    @staticmethod
    @database_return
    def get_level_by_trend(sess_db: Session, ticker: str, trend: str) -> set[Decimal]:
        """Request ticker levels for the selected trend."""
        query: list[Row] = (
            sess_db
            .query(TickerDB.level)
            .filter(
                TickerDB.ticker == ticker, TickerDB.trend == trend)
        ).all()
        return set(map(lambda query: query[0], query))


def transferring_row(table, id: int, ticker: str, level: Decimal, trend: str) -> None:
    """Transfer a row from one table to another."""
    data: dict[str, str | Decimal] = {'ticker': ticker, 'level': level, 'trend': trend}
    Manager.add_to_table(table, data)
    Manager.delete_row(TickerDB, id)


# Create tables in the database defined in the metadata.
Base.metadata.create_all(engine)


# If the stop is not defined, then set the standard one.
if Manager.get_row_by_id(StopVolumeDB, 1) is None:
    Manager.changing_stop(2.5)
    send_message('Added standard stop volume: 2.5 USDT')
