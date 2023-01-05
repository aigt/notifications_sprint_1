from typing import Any, Callable, Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(
    obj_to_serialize: Any,
    *,
    default: Optional[Callable[[Any], Any]],
) -> Any:
    """Функция для сериализации модели в json формат.

    Args:
        obj_to_serialize (Any): Объект для сериализации.
        default (Optional[Callable[[Any], Any]]): Функция для преобразования объекта в поддерживаемый orjson тип.

    Returns:
        Any: получившаяся строка json
    """
    return orjson.dumps(obj_to_serialize, default=default).decode()


class OrjsonModel(BaseModel):
    """Базовый класс для pydantic-моделей c orjson-сериализацией."""

    class Config:
        json_loads = orjson.loads
        json_dumbs = orjson_dumps
