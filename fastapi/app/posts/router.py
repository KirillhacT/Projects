from fastapi import APIRouter, Depends
from app.posts.dao import PostDAO
from app.posts.schemas import SPosts
from app.users.dependencies import get_current_user, get_admin_user

from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/posts",
    tags=['Посты']
)

@router.get("")
@cache(expire=30)
async def get_all_posts(
    user = Depends(get_current_user)
) -> list[SPosts]:
    posts = await PostDAO.find_all()
    return posts

@router.get("/{genre}")
async def get_all_posts_on_genre(
    genre: str,
    user = Depends(get_current_user)
) -> list[SPosts]:
    return await PostDAO.find_all(genre=genre)


@router.post("/add")
async def add_post(
    data: SPosts,
    user = Depends(get_admin_user)
) -> None:
    await PostDAO.add(**dict(data))


@router.delete("/delete")
async def delete_post(
    id: int,
    user = Depends(get_admin_user)
):
    await PostDAO.delete_by_id(id)







