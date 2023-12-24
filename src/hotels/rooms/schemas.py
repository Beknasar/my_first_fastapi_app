# Служит как для валидации данных, так и для представления схемы(структуры данных)
# для генерации тела запроса(request body)
from pydantic import BaseModel


class SRooms(BaseModel):
    id: int
    hotel_id: int
    description: str
    price: int
    services: list
    quantity: int
    image_id: int


class SRoomsTotalCostAndRoomsLeft(SRooms):
    rooms_left: int
    total_cost: int
