# Модели "таблицы" в бэкенде
from src.database import Base
from sqlalchemy import Column, Integer, String, JSON


# В Base будут храниться данные, что у нас есть база данных Hotels
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
