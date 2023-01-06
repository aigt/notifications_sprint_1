from abc import ABC, abstractmethod
from typing import Dict, List, NewType, Optional

from pydantic import BaseModel, Field

TargetWorkerName = NewType("TargetWorkerName", str)
MessageFieldName = NewType("MessageFieldName", str)
MessageFieldValue = NewType("MessageFieldValue", str)


class WorkerMessage(BaseModel):
    """Сообщение с задачей для воркера."""

    # Целевой воркер для обработки
    targets: List[TargetWorkerName] = Field(default=[])
    # Адрес, куда отправить письмо
    email: Optional[str]
    # Шаблон для данной письма
    template: str
    # Набор стандартных полей для шаблона
    fields: Dict[MessageFieldName, MessageFieldValue] = Field(default={})


class Worker(ABC):
    """Воркер выполняющий задачу."""

    @abstractmethod
    def run(self, message: WorkerMessage) -> None:
        """Обработать сообщение.

        Args:
            message (WorkerMessage): Сообщение для обработки.
        """
