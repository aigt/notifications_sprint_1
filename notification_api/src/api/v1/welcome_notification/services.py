from functools import lru_cache

from fastapi import Depends

from models.model_for_queue import Meta, Notification
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
        """
        Формирование данных Welcome уведомления и добавление в очередь.

        Args:
            user_data (WelcomeNotifyRequest): Данные пользователя
        """
        notify_for_queue = Notification(
            meta=Meta(
                urgency="immediate",
                scale="individual",
                email=user_data.email,
                periodic=False,
            ),
            type="welcome",
            fileds={"user_name": user_data.user_name},
        )
        await self.repo.add_in_queue(notify_for_queue)


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
