from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from constant import DATABASE, HOST, PASSWORD, LOGIN

engine = create_engine(
    f'postgresql+psycopg2://{LOGIN}:{PASSWORD}@{HOST}/{DATABASE}', echo=True)
meta = MetaData(schema='public')

conn = engine.connect()

Session = sessionmaker(engine)
sess_db = Session()


class Base(DeclarativeBase):
    metadata = meta
