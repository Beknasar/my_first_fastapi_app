# Для аутентификации пользователя
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from pydantic import EmailStr
from src.users.service import UsersService
from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    # Кодирование JWT
    encoded_jwt = jwt.encode(
        to_encode, os.environ.get("SECRET_KEY"), os.environ.get("ALGORITHM")
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    # Done_TODO 1. Проверка пользователя с текущими данными на существование.
    user = await UsersService.find_one_or_none(email=email)
    if not user and not verify_password(password, user.password):
        return None
    return user

