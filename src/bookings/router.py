# С эндпоинтами вот здесь
from fastapi import APIRouter, Depends
from src.bookings.service import BookingService
from src.bookings.schemas import SBooking
from src.users.dependencies import get_current_user
from src.users.models import Users
from datetime import date
from src.exceptions import RoomCannotBeBookedException

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


# Возвращает журнал записей для зарегистрированного пользователя
@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingService.find_all(user_id=user.id)


# Бронирует номер для пользователя
@router.post("")
async def add_booking(
        room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user),
):
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBookedException


@router.delete("")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingService.delete(booking_id=booking_id, user_id=user.id)

