# С эндпоинтами вот здесь
# from src.hotels.router import router
from fastapi import APIRouter
from src.hotels.rooms.service import RoomsService
from src.hotels.rooms.schemas import SRooms

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int) -> list[SRooms]:
    return await RoomsService.find_all(hotel_id=hotel_id)


# TODO 2. Написать методы для получения, добавления, изменения и удаления записей RoomsService
# @router.delete("/rooms/{room_id}")
# async def delete_room(room_id: int):
#     await RoomsService.delete(room_id)
#     return {"detail": "Room deleted successfully"}
