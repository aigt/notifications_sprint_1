from pydantic import BaseModel, EmailStr


class UserData(BaseModel):
    """Модель данных пользователя из сервиса авторизации."""

    name: str
    email: EmailStr
    telephone: str
