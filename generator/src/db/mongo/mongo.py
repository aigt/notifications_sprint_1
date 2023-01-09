from typing import List, Optional
from uuid import UUID

from bson import Binary
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

    def get_users_by_movie_id(self, movie_id: str) -> List[str]:
        """Запрос для получения списка пользователей подписанных на фильм.

        Args:
            movie_id(str): идентификатор фильма.

        Returns:
            users(List[str]): Список пользователей подписанных на фильм.
        """
        collection = self.client.ugc_movies.bookmark
        return [
            user.get("user_id")
            for user in collection.find({"bookmarks": Binary.from_uuid(UUID(movie_id))})
        ]


def get_mongo() -> MongoDB:
    """Получить объект базы данных.

    Returns:
        MongoDB: Объект базы данных.
    """
    return MongoDB(get_mongo_con())
