# Взаимодействия с БД
from src.bookings.models import Bookings
from src.service.base import BaseService
from sqlalchemy import insert, select, func, and_, or_
from src.hotels.rooms.models import Rooms
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
        """""
        ---ДАТА ЗАЕЗДА '2023-05-15'
        ---ДАТА ВЫЕЗДА '2023-06-20'
        ---Room 1
                    Booking.date_from                    Booking.date_to
                        1 июня                              25 июня
        ----------------|-----------------------------------|------
              ----------|-------------------                |
                        |               --------------------|------------
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
        """""
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
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
            '''''
                SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
                LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
                WHERE rooms.id = 1
                GROUP BY rooms.quantity, booked_rooms.room_id
            '''''
            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left") # label для уточнения
                ).select_from(Rooms).join(
                # мы указали .c потому, что до этого помечали booked rooms через cte
                # вместо ON у нас "," здесь
                    booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                ).where(Rooms.id == room_id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )
            # чтобы нам запринтили ровно так, как это происходит в алхимии, вместо print(rooms_left)
            print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

            rooms_left = await session.execute(get_rooms_left)
            # должно вернуть только одно значение, в данном случае как integer обычный
            # print(rooms_left.scalar())
            rooms_left: int = rooms_left.scalar()
            # чтобы пользователи не могли забронировать номера, если свободных уже нет
            if rooms_left > 0:
                # запрос на получение цены из модели Rooms по конкретной id
                get_price = select(Rooms.price).filter_by(id=room_id)
                # отправляем запрос, и получаем саму цену отеля за один день проживания
                price = await session.execute(get_price)
                # говорим, что
                price: int = price.scalar()
                # запрос на добавление booking'а
                # пишем returning, чтобы в лишний раз потом не обращаться к bookings за новой записью
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                    # В случае, если бы мы возвращали Bookings.id, Bookings.room_id и пр. то,
                    # это уже не отражало бы модель Bookings
                ).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()
                # Здесь мы используем scalar(), т.к. мы возвращаем все поля, отражающие модель Bookings
                # иначе мы бы использовали new_booking.one(), .first(), .one_or_none()
                # или если у нас много запросов .all().
                # А когда у нас возвращаются только модели каки-то фиксированные, которые у нас заданы
                # Например Bookings, Hotels, Rooms, тогда можно воспользоваться .scalars().all()
                return new_booking.scalar()

            else:
                return None
