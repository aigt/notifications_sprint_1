from functools import lru_cache

from fastapi import Depends
from models.welcome_models import WelcomeNotifyRequest
from repositories.base_repository import BaseRepository
from repositories.welcome_notification import WelcomeRepository, get_welcome_repo


class WelcomeService:
    """Сервис ручки для отправки Welcome уведомления."""

    def __init__(self, repo: WelcomeRepository):
        self.repo = repo

    async def add_welcome_notification_in_queue(
        self,
        user_data: WelcomeNotifyRequest,
    ) -> None:
        """Добавление запроса на Welcome уведомление в очередь.

        Args:
            user_data (WelcomeNotifyRequest): Данные пользователя
        """
        await self.repo.add_in_queue(user_data.json())


@lru_cache
def get_welcome_service(
    repository: BaseRepository = Depends(get_welcome_repo),
) -> WelcomeService:
    """Фабрика для сервиса WelcomeService.

    Args:
        repository (BaseRepository): Репозиторий

    Returns:
        WelcomeService: Экземпляр сервиса.
    """
    return WelcomeService(repository)
