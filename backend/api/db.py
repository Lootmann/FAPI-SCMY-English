from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from api.settings import Settings

setting = Settings()

async_engine = create_async_engine(setting.async_db_url, echo=True)
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)


Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
