from cachetools.func import ttl_cache  # type: ignore


@ttl_cache(ttl=15 * 60)  # noqa: WPS432
def get(name: str) -> str:
    """Получить шаблон по названию.

    Args:
        name (str): Название шаблона.

    Returns:
        str: Шаблон.
    """
    return """<!DOCTYPE html>
<html lang="ru">
<head><title>Для информации.</title></head>
<body>
  <h1>{{ title }}</h1>
  <p>{{ text }}</p>
</body>
</html>
"""  # noqa: WPS462
