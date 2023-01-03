import uuid
from http import HTTPStatus

from requests import Session  # type: ignore
from settings import get_settings

settings = get_settings()


def test_welcome_200(http_con: Session) -> None:
    """Проверка работы и возвращаемых данных ендпоинта api/v1/welocme."""

    data = {"user_id": str(uuid.uuid4()), "email": "test_email@gmail.com"}

    response = http_con.post(f"{settings.url}/welcome", json=data)

    assert response.status_code == HTTPStatus.OK
