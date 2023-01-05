import uuid
from http import HTTPStatus

import orjson
from pika.adapters.blocking_connection import BlockingChannel
from requests import Session  # type: ignore
from settings import get_settings
from testdata.testdata import EMAIL

settings = get_settings()


def test_welcome_200(http_con: Session, rabbit_channel: BlockingChannel) -> None:
    """Проверка работы и возвращаемых данных ендпоинта api/v1/welocme."""

    data = {"user_id": str(uuid.uuid4()), "email": EMAIL}

    response = http_con.post(f"{settings.url}/welcome", json=data)
    assert response.status_code == HTTPStatus.OK

    _, _, payload = rabbit_channel.basic_get("Notification")
    payload = orjson.loads(payload)
    assert payload.get("type") == "welcome"

    meta = payload.get("meta")
    assert meta.get("urgency") == "immediate"
    assert meta.get("scale") == "individual"
    assert meta.get("email") == EMAIL
    assert meta.get("periodic") is False


def test_welcome_errors(http_con: Session) -> None:
    """Проверка работы при получении некорректных данных ендпоинтом api/v1/welocme."""

    email = "test_emailgmail.com"
    data = {"useid": 12, "email": email}

    response = http_con.post(f"{settings.url}/welcome", json=data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
