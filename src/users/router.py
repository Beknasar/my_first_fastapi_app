# С endpoint'ами вот здесь
from fastapi import APIRouter, HTTPException, status

from src.users.auth import get_password_hash, verify_password, authenticate_user, create_access_token
from src.users.schemas import SUserAuth
from src.users.service import UsersService

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


# Регистрация пользователя
@router.post("/register")
async def register_user(user_data: SUserAuth):
    # Выполненный тодо 1.  Проверка пользователя с текущими данными на существование
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500)
    # Выполненный тодо 2. Захешировать пароль и добавить в БД
    hashed_password = get_password_hash(user_data.password)
    await UsersService.add(email=user_data.email, hashed_password=hashed_password)


# Логин пользователя
@router.post("/login")
async def auth(user_data: SUserAuth):
    user = authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # Если пользователь есть, создаем токен JWT и отправляем ему в cookie
    access_token = create_access_token({"sub": user.id})
