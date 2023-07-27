from sqladmin import ModelView

from app.users.models import Users
from app.posts.models import Posts, Genres

class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Users.role]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-users"

class PostAdmin(ModelView, model=Posts):
    column_list = [col.name for col in Posts.__table__.c] + [Posts.genre]
    name = "Пост"
    name_plural = "Посты"

class GenreAdmin(ModelView, model=Genres):
    column_list = [col.name for col in Genres.__table__.c] + [Genres.post]
    name = "Жанр"
    name_plural = "Жанры"
