from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import NullPool
from app.config import settings


if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}


engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS) #Движок, используется для создания сессий

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
# Base = declarative_base()
class Base(DeclarativeBase):
    pass