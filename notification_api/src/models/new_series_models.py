from uuid import UUID

from services.orjson import OrjsonModel


class NewSeriesRequest(OrjsonModel):
    """Модель запроса для отправки Welcome письма."""

    movie_id: UUID
