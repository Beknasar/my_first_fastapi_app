# С эндпоинтами вот здесь
from fastapi import APIRouter, Depends
from src.hotels.service import HotelsService
from src.hotels.schemas import SHotels, SHotelsWithRoomsLeft
from datetime import date
from src.exceptions import RoomCannotBeBookedException

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


# логика "рычаг", endpoint
@router.get("")
async def get_hotels(location: str, date_from: date, date_to: date) -> list[SHotelsWithRoomsLeft]:
    return await HotelsService.find_all(location, date_from, date_to)


@router.get("/{hotel_id}/rooms")
async def get_hotel(hotel_id: int) -> SHotels:
    return await HotelsService.find_by_id(hotel_id)


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
