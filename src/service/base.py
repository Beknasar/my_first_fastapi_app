# Базовые взаимодействия с БД

# импортируем создатель(генератор) сессии
from src.database import async_session_maker
from sqlalchemy import select, insert


# Для избежания повторных методов
class BaseService:
    # принимает модели
    model = None

    # Для возврата сущности по id
    @classmethod
    async def find_by_id(cls, model_id: int):
        # открываем сессию с with, чтобы в случае чего сессия закрывалась автоматически
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            # Используем await т.к. мы работаем с асинхронной функцией
            result = await session.execute(query)
            return result.scalar_one_or_none()

    # для неизвестных пользователей например, чтобы проверить есть он или нет
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            # исполни нам запрос по query
            result = await session.execute(query)
            # модель scalar_one_or_none для возврата одного или пустого значения
            return result.scalar_one_or_none()

    # делает запросы к полученной модели
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            # SELECT * FROM bookings;
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    # добавляет новую строку в БД
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            # внести данные по values, как в SQL
            query = insert(cls.model).values(**data)
            await session.execute(query)
            # сохранить изменения
            await session.commit()
