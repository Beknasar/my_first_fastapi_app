# Взаимодествие с БД
from typing import Optional

from src.hotels.models import Hotels
from src.service.base import BaseService
from src.database import engine, async_session_maker
from datetime import date
from src.bookings.models import Bookings
from src.hotels.rooms.models import Rooms
from sqlalchemy import select, func, and_, or_, cast, Integer


class HotelsService(BaseService):
    model = Hotels

    @classmethod
    async def find_all(cls,
                       location: str,
                       date_from: date,
                       date_to: date):
        """
            WITH booked_rooms AS (
                SELECT room_id
                FROM bookings
                WHERE
                    (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                    (date_from <= '2023-05-15' AND date_to > '2023-05-15')
            )
            SELECT
                 hotels.id,
                 hotels.name,
                 hotels.location,
                 hotels.services,
                 hotels.rooms_quantity,
                 hotels.image_id,
                 CAST(hotels.rooms_quantity AS INTEGER) - COUNT(booked_rooms.room_id) AS rooms_left
            FROM hotels
            LEFT JOIN rooms ON rooms.hotel_id = hotels.id
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            WHERE
                hotels.location LIKE '%Алтай%'
            GROUP BY
                hotels.id, hotels.name
            HAVING
                 CAST(hotels.rooms_quantity AS INTEGER) - COUNT(booked_rooms.room_id) > 0;
        """
        async with async_session_maker() as session:
            booked_rooms = select(Bookings.room_id).where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_from > date_from
                    ),
                )
                # подписываем через .cte()
            ).cte("booked_rooms")
            '''''
             SELECT
                 hotels.id,
                 hotels.name,
                 hotels.location,
                 hotels.services,
                 hotels.rooms_quantity,
                 hotels.image_id,
                 CAST(hotels.rooms_quantity AS INTEGER) - COUNT(booked_rooms.room_id) AS rooms_left
            FROM hotels
            LEFT JOIN rooms ON rooms.hotel_id = hotels.id
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            WHERE
                hotels.location LIKE '%Алтай%'
            GROUP BY
                hotels.id, hotels.name
            HAVING
                 CAST(hotels.rooms_quantity AS INTEGER) - COUNT(booked_rooms.room_id) > 0;
            '''''
            get_hotels_with_rooms = select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services,
                Hotels.rooms_quantity,
                Hotels.image_id,
                (cast(Hotels.rooms_quantity, Integer) - func.count(booked_rooms.c.room_id)).label("rooms_left")  # label для уточнения
            ).select_from(Hotels).join(
                    # мы указали .c потому, что до этого помечали booked rooms через cte
                    # вместо ON у нас "," здесь
                    Rooms, Rooms.hotel_id == Hotels.id, isouter=True
                ).join(
                    booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                ).where(Hotels.location.like(f'%{location}%')).group_by(
                    Hotels.id, Hotels.name
                ).having(
                    cast(Hotels.rooms_quantity, Integer) - func.count(booked_rooms.c.room_id) > 0
                )
            # чтобы нам запринтили ровно так, как это происходит в алхимии, вместо print(rooms_left)
            # print(get_hotels_with_rooms.compile(engine, compile_kwargs={"literal_binds": True}))
            hotels_with_rooms = await session.execute(get_hotels_with_rooms)
            # print(hotels_with_rooms.mappings().all())
            return hotels_with_rooms.mappings().all()
