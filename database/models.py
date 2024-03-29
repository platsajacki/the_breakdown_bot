from sqlalchemy import Column, DateTime, Integer, Numeric, String, func

from database.db import Base

numeric_currency = Numeric(precision=21, scale=8)


class BaseColumn:
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    create = Column(DateTime, default=func.now())


class TickerColumn:
    __abstract__ = True

    ticker = Column(String(10))
    level = Column(numeric_currency)
    trend = Column(String(5))
    median_price = Column(numeric_currency, nullable=True)
    update_median_price = Column(DateTime, nullable=True)


class Ticker(Base, BaseColumn, TickerColumn):
    __tablename__ = 'tickers'


class Trend(Base, BaseColumn):
    __tablename__ = 'trend'

    trend = Column(String(5))


class StopVolume(Base, BaseColumn):
    __tablename__ = 'stop_volume'

    usdt_volume = Column(numeric_currency)


class UnsuitableLevels(Base, BaseColumn, TickerColumn):
    __tablename__ = 'unsuitable_levels'


class SpentLevels(Base, BaseColumn, TickerColumn):
    __tablename__ = 'spent_levels'


class OpenedOrder(Base, BaseColumn):
    __tablename__ = 'opened_orders'

    symbol = Column(String(14))
    asset_volume = Column(numeric_currency)
    trigger = Column(numeric_currency)
    entry_point = Column(numeric_currency)
    stop_loss = Column(numeric_currency)
    take_profit = Column(numeric_currency)
