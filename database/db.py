from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from settings.config import DATABASE, HOST, POSTGRES_LOGIN, POSTGRES_PASSWORD

# Configure and connect to the database.
engine: Engine = create_engine(
    f'postgresql+psycopg2://{POSTGRES_LOGIN}:{POSTGRES_PASSWORD}@{HOST}/{DATABASE}',  # noqa: E231
    pool_size=20,
    max_overflow=20,
)
if not database_exists(engine.url):
    create_database(engine.url)

meta = MetaData(schema='public')

SQLSession: sessionmaker[Session] = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    metadata = meta
