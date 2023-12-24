# Взаимодествие с БД
from src.database import async_session_maker, engine
from sqlalchemy import select, func, and_, or_, cast, Integer
from src.bookings.models import Bookings
from src.hotels.rooms.models import Rooms
from src.hotels.models import Hotels
from src.service.base import BaseService
from datetime import date


class RoomsService(BaseService):
    model = Rooms

    @classmethod
    async def find_all(cls,
                       hotel_id: int,
                       date_from: date,
                       date_to: date):
        """
            WITH booked_rooms AS (
                SELECT room_id
                FROM bookings
                WHERE
                    (date_from >= '2023-06-21' AND date_from <= '2023-07-05') OR
                    (date_from <= '2023-07-05' AND date_to > '2023-06-21')
            )
            SELECT
                 Rooms.id,
                 Rooms.hotel_id,
                 Rooms.name,
                 Rooms.description,
                 Rooms.price,
                 Rooms.services,
                 Rooms.quantity,
                 Rooms.image_id,
                 rooms.quantity - COUNT(booked_rooms.room_id) AS rooms_left,
                 Rooms.price * (DATE '2023-07-05' - DATE '2023-06-21') AS total_cost
            FROM rooms
            LEFT JOIN hotels ON rooms.hotel_id = hotels.id
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            WHERE
                hotels.id = 1
            GROUP BY
                Rooms.id, Rooms.name
        """
        async with async_session_maker() as session:
            booked_rooms = select(Bookings.room_id).where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to
                    ),
                    and_(
                        Bookings.date_from <= date_to,  # Начало бронирования до date_to
                        Bookings.date_to > date_from  # Конец бронирования после date_from
                    ),
                )
                # подписываем через .cte()
            ).cte("booked_rooms")
            """""
                 SELECT
                 Rooms.id,
                 Rooms.hotel_id,
                 Rooms.name,
                 Rooms.description,
                 Rooms.price,
                 Rooms.services,
                 Rooms.quantity,
                 Rooms.image_id,
                 rooms.quantity - COUNT(booked_rooms.room_id) AS rooms_left,
                 Rooms.price * (DATE '2023-07-05' - DATE '2023-06-21') AS total_cost
            FROM rooms
            LEFT JOIN hotels ON rooms.hotel_id = hotels.id
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            WHERE
                hotels.id = 1
            GROUP BY
                Rooms.id, Rooms.name
            """""
            get_rooms_by_hotel_id = select(
                Rooms.id,
                Rooms.hotel_id,
                Rooms.name,
                Rooms.description,
                Rooms.price,
                Rooms.services,
                Rooms.quantity,
                Rooms.image_id,
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left"),  # label для уточнения
                (Rooms.price * (func.DATE(date_to) - func.DATE(date_from))).label("total_cost")
            ).select_from(Rooms).join(
                # мы указали .c потому, что до этого помечали booked rooms через cte
                # вместо ON у нас "," здесь
                Hotels, Hotels.id == Rooms.hotel_id, isouter=True
            ).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Hotels.id == hotel_id).group_by(
                Rooms.id, Rooms.name
            )
            # чтобы нам запринтили ровно так, как это происходит в алхимии, вместо print(rooms_left)
            print(get_rooms_by_hotel_id.compile(engine, compile_kwargs={"literal_binds": True}))
            rooms_by_hotel_id = await session.execute(get_rooms_by_hotel_id)
            # print(rooms_by_hotel_id.mappings().all())
            return rooms_by_hotel_id.mappings().all()
