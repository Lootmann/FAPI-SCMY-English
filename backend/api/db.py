from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from api.settings import Settings

setting = Settings()

engine = create_engine(setting.db_url, echo=True)
session = sessionmaker(bind=engine)


Base = declarative_base()


async def get_db():
    async with session() as session:
        yield session
