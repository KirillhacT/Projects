from app.dao.base import BaseDAO
from app.users.models import Users
from app.database import async_session_maker
from sqlalchemy import update


class UserDAO(BaseDAO):
    model = Users

    @classmethod
    async def update_role(cls, email, new_value):
        async with async_session_maker() as session:
            query = update(cls.model).filter_by(email=email).values(role=new_value)
            await session.execute(query)
            await session.commit()

