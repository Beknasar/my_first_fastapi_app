# файл со всеми основными настройками базы данных, здесь происходит подключение к БД и создание некоторых сессии
# для работы с БД, чтобы их не нужно было создавать в других местах
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import DATABASE_URL

# # url Базы данных чтобы помочь алхимии найти где находится база данных
# DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# движок для передачи алхимии
engine = create_async_engine(url=DATABASE_URL)

# генератор сессии (транзакции в БД)
# переменная для работы с БД
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# используется для миграции и сравнении с backend to DB through Alembic
class Base(DeclarativeBase):
    pass
