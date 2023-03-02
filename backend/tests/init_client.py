import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.db import Base, get_db
from api.main import app
from api.settings import Settings

setting = Settings()


@pytest.fixture
def client() -> TestClient:
    engine = create_engine(setting.test_db_url, echo=False)
    session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    def get_test_db():
        try:
            db = session()
            Base.metadata.create_all(bind=engine)
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_test_db

    with TestClient(app=app, base_url="http://test") as client:
        yield client
