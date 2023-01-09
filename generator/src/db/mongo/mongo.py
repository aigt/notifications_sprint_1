from typing import Optional

from pymongo import MongoClient

from core.settings import get_settings
from db.base import BaseDocumentData

settings = get_settings()

mongo_client: Optional[MongoClient] = None


def get_mongo_con() -> MongoClient:
    """Получить клиент базы данных.

    Returns:
        mongo_con(MongoClient): Клиент базы данных.
    """
    return mongo_client


class MongoDB(BaseDocumentData):
    """Класс для работы с MongoDB."""

    def __init__(self, client: MongoClient):
        self.client = client

    def get_user_bookmark(self, user: str) -> None:
        """Запрос закладок пользователя по его имени.

        Args:
            user(str): Почта
        """

    def get_users_by_movie_id(self, movie_id: str) -> None:
        """Запрос для получения списка пользователей подписанных на фильм.

        Args:
            movie_id(str): идентификатор фильма.
        """


def get_mongo() -> MongoDB:
    """Получить объект базы данных.

    Returns:
        MongoDB: Объект базы данных.
    """
    return MongoDB(get_mongo_con())
