from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Literal

load_dotenv()
class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str
    DB_PASS: str

    SECRET_KEY: str
    ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
settings = Settings()

