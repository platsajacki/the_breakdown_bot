from sqlalchemy import Column, DateTime, Integer, Numeric, String, func

from database.database import Base


class BaseColumn:
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    create = Column(DateTime, default=func.now())


class TickerColumn:
    __abstract__ = True

    ticker = Column(String(10))
    level = Column(Numeric(precision=21, scale=8))
    trend = Column(String(5))


class TickerDB(Base, BaseColumn, TickerColumn):
    __tablename__ = 'tickers'


class TrendDB(Base, BaseColumn):
    __tablename__ = 'trend'

    trend = Column(String(5))


class StopVolumeDB(Base, BaseColumn):
    __tablename__ = 'stop_volume'

    usdt_volume = Column(Numeric(precision=21, scale=8))


class UnsuitableLevelsDB(Base, BaseColumn, TickerColumn):
    __tablename__ = 'unsuitable_levels'


class SpentLevelsDB(Base, BaseColumn, TickerColumn):
    __tablename__ = 'spent_levels'


class OpenedOrderDB(Base, BaseColumn):
    __tablename__ = 'opened_orders'

    symbol = Column(String(14))
    asset_volume = Column(Numeric(precision=21, scale=8))
    trigger = Column(Numeric(precision=21, scale=8))
    entry_point = Column(Numeric(precision=21, scale=8))
    stop_loss = Column(Numeric(precision=21, scale=8))
    take_profit = Column(Numeric(precision=21, scale=8))
