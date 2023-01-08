from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Настройки приложения."""

    # Название проекта. Используется в Swagger-документации
    project_name: str = Field(default="Worker")
    app_version: str = "1.0.0"

    # Настройки Rabbitmq
    rb_host: str = Field("localhost")
    rb_port: int = Field(5672)
    rb_user: str = Field("user")
    rb_password: str = Field("pass")
    rb_max_tries_to_connect: int = Field(20)
    rb_connect_retry_period: int = Field(
        default=1,
        description="Период повторных попыток подключения, с",
    )
    rb_worker_queue_name = "worker"
    rb_email_exchange_name = "notifications"
    rb_email_queue_name = "email"
