# Модели "таблицы" в бэкенде
from src.database import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Date, Computed


# В Base будет храниться данные, что у нас есть база данных Bookings
class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, nullable=False, primary_key=True)
    room_id = Column(ForeignKey("rooms.id"))
    user_id = Column(ForeignKey("users.id"))
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Integer, Computed("(date_to - date_from) * price"))
    total_days = Column(Integer, Computed("date_to - date_from"))
