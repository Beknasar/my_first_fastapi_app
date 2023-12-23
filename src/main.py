# Основной файл для запуска приложения. Сюда импортируются все эндпоинты сущностей
import uvicorn
from fastapi import FastAPI, Query
from datetime import date
# для генерации тела запроса(request body)
from pydantic import BaseModel
# чтобы сделать параметры не обязательными
from typing import Optional

from src.bookings.router import router as router_bookings
from src.users.router import router as router_users
from src.hotels.router import router as router_hotels
from src.hotels.rooms.router import router as router_rooms

app = FastAPI()
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)


# автогенерирующийся документация
# http://127.0.0.1:8000/docs


if __name__ == '__main__':
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)

