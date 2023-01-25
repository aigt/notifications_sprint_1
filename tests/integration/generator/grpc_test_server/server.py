from concurrent import futures
from typing import Generator

import grpc
from auth_notify_test_pb2 import UsersDataResponse
from auth_notify_test_pb2_grpc import (
    AuthNotifyServicer,
    add_AuthNotifyServicer_to_server,
)
from users_data import users_data


class Auth(AuthNotifyServicer):
    """Сервис интерфейса gRPC."""

    def GetUserData(self, request, context) -> Generator:
        """Метод для передачи данных клиентов."""
        i = 0
        for user in users_data:
            yield UsersDataResponse(user_id=str(user[0]), email=user[1], name=user[2], telephone=str(user[3]))
            i += 1
            if len(users_data) == i:
                break


def serve():
    """gRPC сервер."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_AuthNotifyServicer_to_server(Auth(), server)
    server.add_insecure_port("[::]:5001")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
