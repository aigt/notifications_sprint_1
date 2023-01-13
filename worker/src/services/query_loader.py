def load_sql(filename: str) -> str:
    """Загрузить SQL запрос из файла.

    Args:
        filename (str): Имя файла с SQL запросом.

    Returns:
        str: Загруженный запрос.
    """
    with open(filename, encoding="utf-8") as query_file:
        query = query_file.read()

    return query
