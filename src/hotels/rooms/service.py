# Взаимодествие с БД
from src.hotels.rooms.models import Rooms
from src.service.base import BaseService


class RoomsService(BaseService):
    model = Rooms

    # @classmethod
    # async def find_all(cls, **filter_by):
    #     pass
