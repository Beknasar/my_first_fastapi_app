# С эндпоинтами вот здесь
from fastapi import APIRouter, Depends
from src.hotels.service import HotelsService
from src.hotels.schemas import SHotels
from datetime import date
from src.exceptions import RoomCannotBeBookedException

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)

# логика "рычаг", endpoint


@router.get("")
async def get_hotels() -> list[SHotels]:
    return await HotelsService.find_all()


@router.get("/{hotel_id}/rooms")
async def get_hotel(hotel_id: int) -> SHotels:
    return await HotelsService.find_by_id(hotel_id)


"""
    WITH booked_rooms AS (
    SELECT room_id
    FROM bookings
    WHERE
        (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
        (date_from <= '2023-05-15' AND date_to > '2023-05-15')
)
SELECT
    hotels.id AS hotel_id,
    hotels.name AS hotel_name,
    COUNT(rooms.id) AS free_rooms_count
FROM hotels
LEFT JOIN rooms ON rooms.hotel_id = hotels.id
LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
WHERE 
	hotels.location LIKE '%Алтай%'
GROUP BY
    hotels.id, hotels.name
HAVING
	SUM(CASE WHEN booked_rooms.room_id IS NULL THEN 1 ELSE 0 END) > 0;
"""


# TODO 1. Написать методы для получения, добавления, изменения и удаления записей HotelsService
# @router.patch("/{hotel_id}/update")
# async def update_hotel(
#         hotel_id: int,
#         name: str,
#         location: str,
#         services: list,
#         rooms_quantity: str,
#         image_id: int,
#         ):
#     return await HotelsService.update(hotel_id, name, location, services, rooms_quantity, image_id)


# @router.delete("/{hotel_id}/delete")
# async def delete_hotel(model_id: int):
#     await HotelsService.delete(model_id)
#     return {"detail": "Hotel deleted successfully"}
