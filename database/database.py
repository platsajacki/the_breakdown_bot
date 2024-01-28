from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from settings import DATABASE, HOST, LOGIN, PASSWORD

# Configure and connect to the database.
engine: Engine = create_engine(f'postgresql+psycopg2://{LOGIN}:{PASSWORD}@{HOST}/{DATABASE}', echo=True)  # noqa: E231
meta: MetaData = MetaData(schema='public')

SQLSession: sessionmaker[Session] = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    metadata = meta
