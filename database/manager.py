from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine.row import Row

from .database import conn, engine, sess_db
from .models import Base, StopVolumeDB, TickerDB, TrendDB
from bot_modules.send_message import send_message
from constants import LONG


class Manager:
    @staticmethod
    def add_to_table(
        table: Base, data: dict[str, Any], commit: bool = True
    ) -> None:
        row: Base = table(**data)
        sess_db.add(row)
        if commit:
            sess_db.commit()

    @staticmethod
    def delete_row(table: Base, id: int, commit: bool = True) -> None:
        row: Base = sess_db.query(table).filter(table.id == id).one()
        sess_db.delete(row)
        if commit:
            sess_db.commit()

    @staticmethod
    def get_all_rows(table: Base) -> CursorResult:
        query: Select = select(table)
        result: CursorResult = conn.execute(query)
        return result

    @staticmethod
    def changing_trend(trend: str) -> None:
        row: TrendDB = sess_db.query(TrendDB).get(1)
        if row is not None:
            row.trend: str = trend
        else:
            row: TrendDB = TrendDB(trend=trend)
            sess_db.add(row)
        sess_db.commit()

    @staticmethod
    def changing_stop(volume: float) -> None:
        row: StopVolumeDB = sess_db.query(StopVolumeDB).get(1)
        if row is not None:
            row.usdt_volume: float = volume
        else:
            row: StopVolumeDB = StopVolumeDB(usdt_volume=volume)
            sess_db.add(row)
        sess_db.commit()

    @staticmethod
    def get_row_by_id(table: Base, id: int) -> Base:
        row: Base = sess_db.query(table).get(id)
        return row

    @staticmethod
    def get_limit_query(
        table: Base, ticker: str, trend: str, limit: int
    ) -> list[dict[str, Any]]:
        query: list[Base] = (
            sess_db.query(table)
            .filter(table.ticker == ticker, table.trend == trend)
            .order_by(table.level if trend == LONG else table.level.desc())
            .limit(limit=limit)
        ).all()
        return [q.__dict__ for q in query]

    @staticmethod
    def select_trend_tickers(trend: str) -> list[Row]:
        query: list[Row] = (
            sess_db.query(TickerDB.ticker).distinct()
            .filter(TickerDB.trend == trend).all()
        )
        return query

    @staticmethod
    def get_current_level(
        ticker: str, trend: str
    ) -> None | dict[str, int | float]:
        level: float = (
            sess_db.query(
                func.min(TickerDB.level) if trend == LONG
                else func.max(TickerDB.level)
            )
            .filter(
                TickerDB.ticker == ticker,
                TickerDB.trend == trend
            )
        ).one_or_none()[0]
        if level is None:
            return None
        rows: dict[str, int | float] = (
            sess_db.query(TickerDB.id, TickerDB.level)
            .filter(
                TickerDB.ticker == ticker,
                TickerDB.level == level)
        ).one()._asdict()
        return rows

    @staticmethod
    def get_level_by_trend(ticker: str, trend: str) -> set[float]:
        query: list[Row] = (
            sess_db
            .query(TickerDB.level)
            .filter(
                TickerDB.ticker == ticker, TickerDB.trend == trend)
        ).all()
        return set(map(lambda query: query[0], query))


def transferring_row(
        table: Base, id: int, ticker: str, level: float, trend: str
):
    data: dict[str, str | float] = {
        'ticker': ticker, 'level': level, 'trend': trend
    }
    Manager.add_to_table(table, data, False)
    Manager.delete_row(TickerDB, id, False)
    sess_db.commit()


Base.metadata.create_all(engine)

if Manager.get_row_by_id(StopVolumeDB, 1) is None:
    Manager.changing_stop(2.5)
    send_message('Added standard stop volume: 2.5 USDT')
