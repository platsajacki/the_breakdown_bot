from sqlalchemy import Column, DateTime, Float, Integer, String, func

from database.database import Base


class BaseColumn:
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    create = Column(DateTime, default=func.now())


class TickerColumn:
    __abstract__ = True

    ticker = Column(String(10))
    level = Column(Float)
    trend = Column(String(5))


class TickerDB(Base, BaseColumn, TickerColumn):
    __tablename__ = 'tickers'


class TrendDB(Base, BaseColumn):
    __tablename__ = 'trend'

    trend = Column(String(5))


class StopVolumeDB(Base, BaseColumn):
    __tablename__ = 'stop_volume'

    usdt_volume = Column(Float)


class UnsuitableLevelsDB(Base, BaseColumn, TickerColumn):
    __tablename__ = 'unsuitable_levels'


class SpentLevelsDB(Base, BaseColumn, TickerColumn):
    __tablename__ = 'spent_levels'


class OpenedOrderDB(Base, BaseColumn):
    __tablename__ = 'opened_orders'

    symbol = Column(String(14))
    asset_volume = Column(Float)
    trigger = Column(Float)
    entry_point = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)
