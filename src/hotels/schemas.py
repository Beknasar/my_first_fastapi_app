# Служит как для валидации данных, так и для представления схемы(структуры данных)
# для генерации тела запроса(request body)
from pydantic import BaseModel


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: list
    rooms_quantity: int
    image_id: int


class SHotelsWithRoomsLeft(SHotels):
    rooms_left: int
