from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from api.settings import Settings

setting = Settings()

engine = create_engine(setting.db_url, echo=True)
session = sessionmaker(bind=engine)


Base = declarative_base()


def get_db():
    with session() as Session:
        yield Session
