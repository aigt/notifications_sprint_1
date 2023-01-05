from abc import ABC, abstractmethod
from typing import Dict, List, NewType, TypedDict

TargetWorkerName = NewType("TargetWorkerName", str)
MessageFieldName = NewType("MessageFieldName", str)
MessageFieldValue = NewType("MessageFieldValue", str)


class WorkerMessage(TypedDict):
    """Сообщение с задачей для воркера."""

    # Целевой воркер для обработки
    target: List[TargetWorkerName]
    # Адрес, куда отправить письмо
    email: str
    # Шаблон для данной письма
    template: str
    # Набор стандартных полей для шаблона
    fields: Dict[MessageFieldName, MessageFieldValue]


class Worker(ABC):
    """Воркер выполняющий задачу."""

    @abstractmethod
    def run(self, message: WorkerMessage) -> None:
        """Обработать сообщение.

        Args:
            message (WorkerMessage): Сообщение для обработки.
        """
