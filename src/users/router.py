# С endpoint'ами вот здесь
from fastapi import APIRouter, Response, Depends
from src.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from src.users.auth import get_password_hash, authenticate_user, create_access_token
from src.users.dependencies import get_current_user, get_current_admin_user
from src.users.models import Users
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
        raise UserAlreadyExistsException
    # Выполненный тодо 2. Захешировать пароль и добавить в БД
    hashed_password = get_password_hash(user_data.password)
    await UsersService.add(email=user_data.email, hashed_password=hashed_password)


# Логин уже зарегистрированного пользователя, чтобы у него был доступ к эндпоинтам
@router.post("/login")
async def auth(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    # Если пользователь есть, создаем токен JWT и отправляем ему в cookie
    access_token = create_access_token({"sub": str(user.id)})
    # засетить cookie, т.е. токен доступа для приложения booking
    # httponly, чтобы никто не мог получить токен по js и зайти под чужим именем
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


# Для выхода пользователей из учётной записи удаляется куки
@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    return "Пользователь вышел из учётной записи"


# Для получения информации о текущем пользователе
@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


# Для получения данных о всех пользователях
@router.get("/all")
async def read_users_all(current_user: Users = Depends(get_current_admin_user)):
    return await UsersService.find_all()
