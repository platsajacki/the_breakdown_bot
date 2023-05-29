from peewee import *
from keys import database, user, password, host

db = PostgresqlDatabase(database, user=user, password=password, host=host)


class BaseModel(Model):
    class Meta:
        database = db


class TickerDB(BaseModel):
    ticker = CharField(max_length=6)
    level = FloatField()
    trend = CharField(max_length=5)

    class Meta:
        db_table = 'tickers'

    def get_long_tickers() -> list:
        query = TickerDB.select(
            fn.Distinct(TickerDB.ticker)).where(TickerDB.trend == 'long')
        long_tickers = []
        for long_ticker in query:
            long_tickers.append(long_ticker.ticker)
        return long_tickers

    def get_short_tickers() -> list:
        query = TickerDB.select(
            fn.Distinct(TickerDB.ticker)).where(TickerDB.trend == 'short')
        short_tickers = []
        for short_ticker in query:
            short_tickers.append(short_ticker.ticker)
        return short_tickers

    def get_tickers_level() -> list:
        query = TickerDB.select().dicts()
        row_list = []
        for row in query:
            row_list.append(row)
        return row_list

    def get_min_long_lvl(ticker) -> dict:
        query = TickerDB.select(
            TickerDB.id,
            TickerDB.level).where(
            TickerDB.ticker == ticker,
            TickerDB.level == (
                TickerDB.select(fn.min(TickerDB.level)).where(
                    TickerDB.ticker == ticker,
                    TickerDB.trend == 'long'))).dicts()
        for row in query:
            return row

    def get_max_short_lvl(ticker) -> dict:
        query = TickerDB.select(
            TickerDB.id,
            TickerDB.level).where(
            TickerDB.ticker == ticker,
            TickerDB.level == (
                TickerDB.select(fn.max(TickerDB.level)).where(
                    TickerDB.ticker == ticker,
                    TickerDB.trend == 'short'))).dicts()
        for row in query:
            return row

    def delete_row(id):
        TickerDB.get(TickerDB.id == id).delete_instance()


class TrendDB(BaseModel):
    trend = CharField(max_length=5)

    class Meta:
        db_table = 'trend'

    def get_trend() -> str:
        query = TrendDB.get(TrendDB.id == 1)
        return query.trend


class StopVolumeDB(BaseModel):
    usdt_volume = FloatField()

    class Meta:
        db_table = 'stop_volume'

    def create_or_save_stop(volume):
        query = StopVolumeDB.get_or_none(StopVolumeDB.id == 1)
        if query is None:
            StopVolumeDB(usdt_volume=volume).save()
        else:
            StopVolumeDB(id=1, usdt_volume=volume).save()

    def get_stop_volume() -> float:
        query = StopVolumeDB.get(StopVolumeDB.id == 1)
        return query.usdt_volume


class UnsuitableLevelsDB(BaseModel):
    ticker = CharField(max_length=6)
    level = FloatField()
    trend = CharField(max_length=5)

    class Meta:
        db_table = 'unsuitable_levels'


class SpentLevelsDB(BaseModel):
    ticker = CharField(max_length=6)
    level = FloatField()
    trend = CharField(max_length=5)

    class Meta:
        db_table = 'spent_levels'


class OpenedOrderDB(BaseModel):
    symbol = CharField(max_length=12)
    asset_volume = FloatField()
    trigger = FloatField()
    entry_point = FloatField()
    stop_loss = FloatField()
    take_profit = FloatField()

    class Meta:
        db_table = 'opened_orders'


db.create_tables([
    TickerDB,
    TrendDB,
    StopVolumeDB,
    UnsuitableLevelsDB,
    SpentLevelsDB,
    OpenedOrderDB
])
