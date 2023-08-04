from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from package import *
from redis import asyncio as aioredis

from sqladmin import Admin, ModelAdmin, ModelView

from app.admin.auth import authentication_backend
from app.admin.views import GenreAdmin, PostAdmin, UsersAdmin

from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.posts.router import router as router_posts
from app.users.router import router as router_users
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), "static")

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_pages)
app.include_router(router_posts)
app.include_router(router_images)


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(PostAdmin)
admin.add_view(GenreAdmin)

