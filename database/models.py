from sqlalchemy import Column, Integer, Float, String, DateTime, func
from .database import Base, engine


class IdColumn():
    __abstract__ = True

    id = Column(Integer, primary_key=True)


class TickerColumn():
    __abstract__ = True

    ticker = Column(String(10))
    level = Column(Float)
    trend = Column(String(5))
    create = Column(DateTime, default=func.now())


class TickerDB(Base, IdColumn, TickerColumn):
    __tablename__ = 'tickers'


class TrendDB(Base, IdColumn):
    __tablename__ = 'trend'

    trend = Column(String(5))


class StopVolumeDB(Base, IdColumn):
    __tablename__ = 'stop_volume'

    usdt_volume = Column(Float)


class UnsuitableLevelsDB(Base, IdColumn, TickerColumn):
    __tablename__ = 'unsuitable_levels'


class SpentLevelsDB(Base, IdColumn, TickerColumn):
    __tablename__ = 'spent_levels'


class OpenedOrderDB(Base, IdColumn):
    __tablename__ = 'opened_orders'

    symbol = Column(String(14))
    asset_volume = Column(Float)
    trigger = Column(Float)
    entry_point = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)
    create = Column(DateTime, default=func.now())


Base.metadata.create_all(engine)
