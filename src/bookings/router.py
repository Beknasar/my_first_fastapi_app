# С эндпоинтами вот здесь
from fastapi import APIRouter, Depends
from src.bookings.service import BookingService
from src.bookings.schemas import SBooking
from src.users.dependencies import get_current_user
from src.users.models import Users

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
        user: Users = Depends(get_current_user),
):
    await BookingService.add(user_id=user.id)
