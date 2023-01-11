from pymongo import MongoClient
from pymongo.collection import Collection
from testdata import mongo_data


def add_test_data_bookmark(mongo_client: MongoClient) -> None:
    """Добавление тестовых данных в коллекцию bookmark"""
    collection: Collection = mongo_client.ugc_movies.bookmark
    collection.insert_many((mongo_data.bookmark_1, mongo_data.bookmark_2))
