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

app = FastAPI()
app.include_router(router_users)
app.include_router(router_bookings)

# автогенерирующийся документация
# http://127.0.0.1:8000/docs

# схема отеля
class SHotel(BaseModel):
    address: str
    name: str
    stars: int


# логика "рычаг", endpoint
@app.get("/hotels", response_model=list[SHotel])
def get_hotels(
    location: str,
    date_from: date,
    date_to: date,
    # опциональные параметры
    # has_spa: Optional[bool] = None,
    # stars: Optional[int] = Query(None, ge=1, le=5),
    has_spa: bool = None,
    stars: int = Query(None, ge=1, le=5),
) -> list[SHotel]:
    hotels = [
        {
            "address": "ул. Горькое, 6, Бишкек",
            "name": "International",
            "stars": 3,
        },
    ]
    return hotels


if __name__ == '__main__':
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)

