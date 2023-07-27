from fastapi import UploadFile, APIRouter
import shutil

router = APIRouter(
    prefix="/images",
    tags=['Загрузка картинок']
)

@router.post("/posts")
async def add_post_image(name: int, file: UploadFile):
    with open(f"static/images/{name}.webp", "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

