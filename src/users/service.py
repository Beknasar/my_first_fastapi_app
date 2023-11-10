# Взаимодествие с БД
from src.users.models import Users
from src.service.base import BaseService


class UsersService(BaseService):
    model = Users
