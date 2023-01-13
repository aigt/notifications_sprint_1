from typing import Generator

import pymongo
from pymongo import MongoClient
from pytest import fixture
from settings import get_settings
from utils.add_mongo_data import add_test_data_bookmark


@fixture(scope="session")
def mongo_con() -> Generator:
    """Соединение с MongoDB"""

    client: pymongo.MongoClient = pymongo.MongoClient(get_settings().mongo_dsn, uuidRepresentation="standard")
    yield client
    client.close()


@fixture(scope="function")
def add_bookmark(mongo_con: MongoClient) -> Generator:
    """Фикстура для загрузки и очистки данных из коллекции bookmark."""
    add_test_data_bookmark(mongo_con)
    yield
    mongo_con.ugc_movies.bookmark.drop()
