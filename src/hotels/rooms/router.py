# С эндпоинтами вот здесь
from fastapi import APIRouter, Depends
from src.hotels.router import router
from src.bookings.service import BookingService
from src.bookings.schemas import SBooking
from src.users.dependencies import get_current_user
from src.users.models import Users
from datetime import date
from src.exceptions import RoomCannotBeBookedException


@router.get("/{hotel_id}/rooms")
def get_rooms():
    pass
