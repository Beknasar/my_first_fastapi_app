# Служит как для валидации данных, так и для представления схемы(структуры данных)
from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str
