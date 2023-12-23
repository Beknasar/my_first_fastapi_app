# Взаимодествие с БД
from typing import Optional

from src.hotels.models import Hotels
from src.service.base import BaseService
from src.database import engine, async_session_maker
from datetime import date


class HotelsService(BaseService):
    model = Hotels

    @classmethod
    async def find_all(cls,
        location: str,
        date_from: date,
        date_to: date):
        pass

