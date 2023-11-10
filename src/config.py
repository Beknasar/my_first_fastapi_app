# Все данные о подключении к БД, к Redis, к почте и т.д.
from pydantic_settings import BaseSettings
from pydantic import root_validator
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")

# url Базы данных чтобы помочь алхимии найти где находится база данных
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# class Settings(BaseSettings):
#     DB_HOST: str
#     DB_PORT: int
#     DB_USER: str
#     DB_PASS: str
#     DB_NAME: str
#
#     @root_validator
#     def get_database_url(cls, v):
#         v['DATABASE_URL'] = f"postgresql+asyncpg://{v.DB_USER}:{v.DB_PASS}@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
#         return v
#
#     class Config:
#         env_file = ".env"
#
#
# settings = Settings()
# print(settings.DATABASE_URL)
