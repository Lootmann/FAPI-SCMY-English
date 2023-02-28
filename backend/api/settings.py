from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url: str
    async_db_url: str
    test_db_url: str

    class Config:
        env_file = ".env"
