from pydantic import BaseSettings


class Settings(BaseSettings):
    async_db_url: str
    test_db_url: str

    class Config:
        env_file = ".env"
