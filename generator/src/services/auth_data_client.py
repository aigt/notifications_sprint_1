from typing import Generator
import grpc

from grpcs import auth_notify_pb2_grpc
from pydantic import BaseModel


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
        """Получить данные пользователей

        Yields:
            Generator[User, None, None]: Стрим получаемых данных.
        """
        with grpc.insecure_channel(self._host) as channel:
            stub = auth_notify_pb2_grpc.AuthNotifyStub(channel=channel)

            for user in stub.GetUserData():
                yield User(
                    user_id=user.user_id,
                    name=user.name,
                    email=user.email,
                    telephone=user.telephone,
                )
