# Файл с ошибками, чтобы было более подробное описание ошибок
from fastapi import HTTPException, status


# Сначала задаем базовое исключение BookingException для всего
# приложения, от которого мы будем наследоваться.
class BookingException(HTTPException):  # <-- наследуемся от HTTPException,
    # который наследован от Exception
    # Мы указываем значения по умолчанию,
    # которые будут использоваться в классах-потомках, если их не задавать
    status_code = 500
    detail = ""

    # Мы также переписываем магический метод __init__ ,
    # который вызывает HTTPException с заданными нами параметрами
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(HTTPException):  # <-- обязательно наследуемся от нашего класса
    status_code = status.HTTP_409_CONFLICT,
    detail = "Пользователь уже существует",


class IncorrectEmailOrPasswordException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Неверная почта или пароль",


class TokenExpiredException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Токен истек",


class TokenAbsentException(HTTPException):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail = "Токен отсутствует",


class IncorrectTokenFormatException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Некорректный формат токена",

# если пользователя нет
class UserIsNotPresentException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED,

