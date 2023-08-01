from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from constants import DATABASE, HOST, LOGIN, PASSWORD

engine: Engine = create_engine(
    f'postgresql+psycopg2://{LOGIN}:{PASSWORD}@{HOST}/{DATABASE}', echo=True
)
meta: MetaData = MetaData(schema='public')

conn: Connection = engine.connect()

Session: sessionmaker = sessionmaker(engine)
sess_db: Session = Session()


class Base(DeclarativeBase):
    metadata: MetaData = meta
