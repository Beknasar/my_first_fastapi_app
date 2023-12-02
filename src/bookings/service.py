# Взаимодействия с БД
from src.bookings.models import Bookings
from src.service.base import BaseService
from sqlalchemy import delete, insert, select, func, and_, or_
from src.rooms.models import Rooms
from src.database import engine, async_session_maker
from datetime import date


class BookingService(BaseService):
    model = Bookings

    # переписываем функцию add из service/base
    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date,
    ):
        """
        ---ДАТА ЗАЕЗДА '2023-05-15'
        ---ДАТА ВЫЕЗДА '2023-06-20'
        ---Room 1
        создаем переменную в котором хранятся данные о бронированиях, где номер комнаты раувна = 1
        и где временные промежутки:
         date_from больше чем дата заезда и меньше чем дата выезда или
        где date_from меньше чем дата заезда и date_to больше чем дата выезда

        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
            (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == 1,
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
                )
                # подписываем через .cte()
            ).cte("booked_rooms")
            '''
                SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
                LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
                WHERE rooms.id = 1
                GROUP BY rooms.quantity, booked_rooms.room_id
            '''
            rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left") # label для уточнения
                ).select_from(Rooms).join(
                # мы указали .c потому, что до этого помечали booked rooms через cte
                # вместо ON у нас "," здесь
                    booked_rooms, booked_rooms.c.room_id == Rooms.id
                ).where(Rooms.id == 1).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )
            # чтобы нам запринтили ровно так, как это происходит в алхимии
            print(rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

            rooms_left = await session.execute(rooms_left)
            print(rooms_left.scalar())
