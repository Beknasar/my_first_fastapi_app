from fastapi import UploadFile, APIRouter
import shutil # т.к. файл находится в оперативной памяти, а не в ЖД, нужно его сохранить в нашу папку


router = APIRouter(
    prefix="/images",
    tags=['Загрузка картинок']
)

# добавляет загруженную картинку в static images
@router.post('/hotels')
async def add_hotel_image(name: int, file: UploadFile):
    with open(f"src/static/images/{name}.webp", "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
