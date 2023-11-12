import os
from datetime import datetime
from src.users.service import UsersService
from fastapi import Request, HTTPException, Depends, status
from jose import  jwt, JWTError


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
    expire: str = payload.get("exp")
    expire_decode = datetime.utcfromtimestamp(expire)
    # если нет expire или он истёк
    if (not expire_decode) or (expire_decode < datetime.utcnow()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_id: str = payload.get("sub")
    # если нет id пользователя
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await UsersService.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
