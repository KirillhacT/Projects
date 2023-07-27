from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings

#Здесь идет подключение к бд

engine = create_async_engine(settings.DATABASE_URL) #Движок, используется для создания сессий

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
# Base = declarative_base()
class Base(DeclarativeBase):
    pass