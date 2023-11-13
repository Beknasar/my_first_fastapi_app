import os
from datetime import datetime

from src.users.models import Users
from src.users.service import UsersService
from fastapi import Request, HTTPException, Depends, status
from jose import jwt, JWTError


# Выдает токен
def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


# возвращает пользователя по token
# Depends - зависит, в данном случае от функции get_token
async def get_current_user(token: str = Depends(get_token)):
    try:
        # Декодирование JWT
        payload = jwt.decode(
            token, os.environ.get("SECRET_KEY"), os.environ.get("ALGORITHM")
        )
    # если JWT токен не является действительным
        print(payload)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # Извлечение значения 'exp' из декодированного JWT
    expire: float = payload.get("exp")
    # если нет expire или он истёк
    if (not expire) or (expire < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # if not expire or jwt.ExpiredSignatureError:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_id: str = payload.get("sub")
    # если нет id пользователя
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await UsersService.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


# Для проверки роли пользователя на админа, потом эту зависимость можно прокинуть на "эндпоинт"
# к которому должен быть доступ только у админа.
# Например, создание других пользователей или просмотр данных о всех пользователях т.д.
async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    # К сожалению пока поля role в модели users нету
    # if current_user.role != "admin":
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return current_user
