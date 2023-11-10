# Модели "таблицы" в бэкенде
from src.database import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey


# В Base будет храниться данные, что у нас есть база данных Hotels
class Rooms(Base):
    __tablename__ = "rooms"
    id = Column(Integer, nullable=False, primary_key=True)
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    services = Column(JSON, nullable=True)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)
