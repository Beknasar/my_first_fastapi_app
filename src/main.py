# Основной файл для запуска приложения. Сюда импортируются все эндпоинты сущностей
import uvicorn
from fastapi import FastAPI, Query

from fastapi.staticfiles import StaticFiles
# для генерации тела запроса(request body)
from pydantic import BaseModel
# чтобы сделать параметры не обязательными
from typing import Optional

from starlette.middleware.cors import CORSMiddleware

from src.bookings.router import router as router_bookings
from src.users.router import router as router_users
from src.hotels.router import router as router_hotels
from src.hotels.rooms.router import router as router_rooms
from src.images.router import router as router_images

from src.pages.router import router as router_pages

app = FastAPI()

app.mount('/static', StaticFiles(directory="src/static"), "static")

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)

app.include_router(router_pages)
app.include_router(router_images)
# автогенерирующийся документация
# http://127.0.0.1:8000/docs

origins = [
    "http://localhost:3000",
    # https://mysite.com
]  # Добавление площадок, которые могут обращаться к нашим API

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # передали список площадок
    allow_credentials=True,  # отвечает за Cookie. Если стоит True,
    # то с каждым запросом будет посылаться Cookie, которые у нас записаны в Cookaх.
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],  # Если продакшен, то нужно описать какие именно методы используются.
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Authorization"],  # То же самое, только Headers.
)

if __name__ == '__main__':
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)

