# С эндпоинтами вот здесь
# from src.hotels.router import router
from fastapi import APIRouter, Query
from datetime import date, datetime
from src.hotels.rooms.service import RoomsService
from src.hotels.rooms.schemas import SRooms, SRoomsTotalCostAndRoomsLeft

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_time(
        hotel_id: int,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {datetime.now().date()}")
) -> list[SRoomsTotalCostAndRoomsLeft]:
    return await RoomsService.find_all(hotel_id, date_from, date_to)

# TODO 2. Написать методы для получения, добавления, изменения и удаления записей RoomsService
# @router.delete("/rooms/{room_id}")
# async def delete_room(room_id: int):
#     await RoomsService.delete(room_id)
#     return {"detail": "Room deleted successfully"}
