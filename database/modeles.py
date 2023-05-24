from peewee import *
from keys import database, user, password, host

db = PostgresqlDatabase(database, user=user, password=password, host=host)


class BaseModel(Model):
    class Meta:
        database = db


class TickerDB(BaseModel):
    ticker = CharField(max_length=6)
    price_lvl = FloatField()
    trend = CharField(max_length=5)

    class Meta:
        db_table = 'tickers'

    def get_long_tickers():
        query = TickerDB.select(
            fn.Distinct(TickerDB.ticker)).where(TickerDB.trend == 'long')
        long_tickers = []
        for long_ticker in query:
            long_tickers.append(long_ticker.ticker)
        return long_tickers

    def get_short_tickers():
        query = TickerDB.select(
            fn.Distinct(TickerDB.ticker)).where(TickerDB.trend == 'short')
        short_tickers = []
        for short_ticker in query:
            short_tickers.append(short_ticker.ticker)
        return short_tickers


class TrendDB(BaseModel):
    trend = CharField(max_length=5)

    class Meta:
        db_table = 'trend'

    def get_trend():
        query = TrendDB.get(TrendDB.id == 1)
        return query.trend
