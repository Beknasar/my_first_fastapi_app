# Служит как для валидации данных, так и для представления схемы(структуры данных)
from datetime import date

from pydantic import BaseModel


class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    # Показать Pydantic, что к модели можно обращаться как к классу
    class Config:
        orm_mode = True
