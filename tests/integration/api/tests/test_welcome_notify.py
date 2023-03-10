from http import HTTPStatus

import orjson
from pika.adapters.blocking_connection import BlockingChannel
from requests import Session  # type: ignore
from settings import get_settings
from testdata.testdata import data_welcome

settings = get_settings()


def test_add_notification_welcome_200(http_con: Session, rabbit_channel: BlockingChannel) -> None:
    """Проверка работы и возвращаемых данных ендпоинта api/v1/welocme."""

    response = http_con.post(f"{settings.url}/add_notification", json=data_welcome)
    assert response.status_code == HTTPStatus.OK
    for method_frame, _, payload in rabbit_channel.consume(settings.rb_emails_queue, auto_ack=True):
        payload = orjson.loads(payload)

        assert payload.get("email") == data_welcome.get("fields").get("email")
        if method_frame.delivery_tag == 1:
            break


def test_welcome_errors(http_con: Session) -> None:
    """Проверка работы при получении некорректных данных ендпоинтом api/v1/welocme."""

    email = "test_emailgmail.com"
    data = {"useid": 12, "email": email}

    response = http_con.post(f"{settings.url}/add_notification", json=data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
