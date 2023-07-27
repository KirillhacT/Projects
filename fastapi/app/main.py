from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from package import *
from app.database import engine
from app.config import settings

#routers
from app.bookings.router import router as router_bookings 
from app.users.router import router as router_users
from app.pages.router import router as router_pages
from app.posts.router import router as router_posts
from app.images.router import router as router_images

#redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

#sqladmin
from sqladmin import Admin, ModelView, ModelAdmin
from app.admin.views import UsersAdmin, PostAdmin, GenreAdmin
from app.admin.auth import authentication_backend

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

