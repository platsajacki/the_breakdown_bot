from sqlalchemy import select, func
from .database import sess_db, conn, engine
from .models import Base, TickerDB, TrendDB, StopVolumeDB
from bot_modules.send_message import send_message


class Manager():
    @staticmethod
    def add_to_table(table, data):
        row = table(**data)
        sess_db.add(row)
        sess_db.commit()

    @staticmethod
    def delete_row(table, id):
        row = sess_db.query(table).filter(table.id == id).one()
        sess_db.delete(row)
        sess_db.commit()

    @staticmethod
    def get_all_rows(table):
        query = select(table)
        result = conn.execute(query)
        return result

    @staticmethod
    def changing_trend(trend):
        row = sess_db.query(TrendDB).get(1)
        if row is not None:
            row.trend = trend
        else:
            row = TrendDB(trend=trend)
            sess_db.add(row)
        sess_db.commit()

    @staticmethod
    def changing_stop(volume):
        row = sess_db.query(StopVolumeDB).get(1)
        if row is not None:
            row.usdt_volume = volume
        else:
            row = StopVolumeDB(usdt_volume=volume)
            sess_db.add(row)
        sess_db.commit()

    @staticmethod
    def get_row_by_id(table, id):
        row = sess_db.query(table).get(id)
        return row

    @staticmethod
    def select_trend_tickers(trend):
        query = (
            sess_db.query(TickerDB.ticker).distinct()
            .filter(TickerDB.trend == trend).all()
        )
        return query

    @staticmethod
    def get_current_level(ticker, trend):
        level = None
        if trend == 'long':
            level = (
                sess_db.query(func.min(TickerDB.level))
                .filter(
                    TickerDB.ticker == ticker,
                    TickerDB.trend == trend)
            ).one_or_none()[0]
        else:
            level = (
                sess_db.query(func.max(TickerDB.level))
                .filter(
                    TickerDB.ticker == ticker,
                    TickerDB.trend == trend)
            ).one_or_none()[0]
        if level is None:
            return None
        row = (
            sess_db.query(TickerDB.id, TickerDB.level)
            .filter(
                TickerDB.ticker == ticker,
                TickerDB.level == level)
        ).one()._asdict()
        return row


Base.metadata.create_all(engine)

if Manager.get_row_by_id(StopVolumeDB, 1) is None:
    Manager.changing_stop(2.5)
    send_message('Added standard stop volume: 2.5 USDT')
