from typing import Optional

from db.base import BaseDocumentData
from pymongo import MongoClient

from core.settings import get_settings

settings = get_settings()

mongo_client: Optional[MongoClient] = None


def get_mongo_con() -> MongoClient:
    """Получить объект базы данных.

    Returns:
        mongo_con(MongoClient): Клиент базы данных.
    """
    return mongo_client


class MongoDB(BaseDocumentData):
    """Класс для работы с MongoDB."""

    def get_user_bookmark(self, user: str) -> None:
        """Запрос закладок пользователя по его имени.

        Args:
            user(str): Почта
        """
