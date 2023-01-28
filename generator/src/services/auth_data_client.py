from typing import Generator, List

import grpc
import orjson
from pydantic import BaseModel

from grpcs import auth_notify_pb2, auth_notify_pb2_grpc


class User(BaseModel):
    """Модель данных пользователя."""

    user_id: str
    name: str
    email: str
    telephone: str


class AuthDataClient:
    """Клиент получающий данные от Auth сервиса."""

    def __init__(self, host: str) -> None:
        self._host = host

    def users_data(self) -> Generator[User, None, None]:
        """Получить данные пользователей.

        Yields:
            Generator[User, None, None]: Стрим получаемых данных.
        """
        with grpc.insecure_channel(self._host) as channel:
            stub = auth_notify_pb2_grpc.AuthNotifyStub(channel=channel)

            for user in stub.GetUserData(auth_notify_pb2.UsersDataRequest()):  # noqa: WPS526
                yield User(
                    user_id=user.user_id,
                    name=user.name,
                    email=user.email,
                    telephone=user.telephone,
                )

    def users_data_from_ids(self, users_ids: List[str]) -> Generator[User, None, None]:
        """Получить данные пользователей по их id.

        Args:
            users_ids(List[str]): Список пользователей, чъю почту необходимо получить.

        Yields:
            Generator[User, None, None]: Стрим получаемых данных.
        """
        users_ids = orjson.dumps(users_ids)
        with grpc.insecure_channel(self._host) as channel:
            stub = auth_notify_pb2_grpc.AuthNotifyStub(channel=channel)

            for user in stub.GetUserDataFromUsersId(auth_notify_pb2.UsersIds(list_ids=users_ids)):  # noqa: WPS526
                yield User(
                    user_id=user.user_id,
                    name=user.name,
                    email=user.email,
                    telephone=user.telephone,
                )
