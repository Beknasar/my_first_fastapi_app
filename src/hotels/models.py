# Модели "таблицы" в бэкенде
from src.database import Base
from sqlalchemy import Column, Integer, String, JSON


# В Base будет хранится данные, что у нас есть база данных Hotels
class Hotels(Base):
    __tablename__ = "hotels"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(String, nullable=False)
    image_id = Column(Integer)
