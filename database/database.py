from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from constants import DATABASE, HOST, LOGIN, PASSWORD

# Configure and connect to the database.
engine: Engine = create_engine(f'postgresql+psycopg2://{LOGIN}:{PASSWORD}@{HOST}/{DATABASE}', echo=True)
meta: MetaData = MetaData(schema='public')

Session: sessionmaker = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    metadata: MetaData = meta
