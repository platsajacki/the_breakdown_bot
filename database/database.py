from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from keys import database, host, password, user

engine = create_engine(
    f'postgresql+psycopg2://{user}:{password}@{host}/{database}', echo=True)
meta = MetaData(schema='public')

conn = engine.connect()

Session = sessionmaker(engine)
sess_db = Session()


class Base(DeclarativeBase):
    metadata = meta
