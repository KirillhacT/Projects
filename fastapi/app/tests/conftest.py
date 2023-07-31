import pytest
import json
from sqlalchemy import insert
import asyncio
from datetime import datetime

from app.database import Base, async_session_maker, engine
from app.config import settings 
from app.posts.models import Posts, Genres
from app.users.models import Users
from app.bookings.models import Bookings

@pytest.fixture(scope="session", autouse=True) #Подготавливает среду для тестирования
async def prepare_database():   
    await asyncio.sleep(0)
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json") as file:
            return json.load(file)
    posts = open_mock_json("posts")
    for post in posts:
        post["release_date"] = datetime.strftime(post["release_data"], "%Y-%m-%d")

    # genres = open_mock_json("genres")
    # users = open_mock_json("users")
    # bookings = open_mock_json("bookings")
    async with async_session_maker() as session:
        add_posts = insert(Posts).values(posts)
        await session.execute(add_posts)
        await session.commit()

@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()






