from app.dao.base import BaseDAO
from app.posts.models import Posts

class PostDAO(BaseDAO):
    model = Posts        