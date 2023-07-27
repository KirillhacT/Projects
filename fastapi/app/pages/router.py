from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.posts.router import get_all_posts

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)
templates = Jinja2Templates(directory="templates")

@router.get("/posts")
async def get_posts_page(
    request: Request,
    posts=Depends(get_all_posts)
):
    return templates.TemplateResponse(
        name="index.html", 
        context={"request": request, "posts": posts}
    )
