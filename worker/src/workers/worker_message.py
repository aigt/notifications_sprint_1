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
    # Телефин, куда отправить SMS
    telephone: Optional[str]
    # push_id, куда отправить push уведомление
    push_id: Optional[str]
    # Для сохранения в историю оповещений
    user_id: Optional[str]
    # Шаблон для данной письма
    template: str
    # Набор стандартных полей для шаблона
    fields: Dict[MessageFieldName, MessageFieldValue] = Field(default={})
