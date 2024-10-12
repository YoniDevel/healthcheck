import logging
from pymongo import AsyncMongoClient
from typing import Mapping, TypeVar
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.collection import AsyncCollection

from src.config import parsed_config


class DBInternals():
    def __init__(self, client: AsyncMongoClient | None = None, dbs: dict = {}) -> None:
        self.client = client
        self.dbs = dbs

internals = DBInternals()

T = TypeVar('T', bound=Mapping[str, None])

def connect_client() -> None:
    if not internals.client:
        internals.client = AsyncMongoClient(str(parsed_config.MONGO_URI))

def connect_db(db_name: str) -> None:
    if not internals.client:
        logging.error('Cannot connect to db because client does not exist')
        raise Exception('Cannot connect to db because client does not exist')
    internals.dbs[db_name] = (internals.client[db_name])

def get_collection(collection_name: str, db_name: str = parsed_config.DB_NAME) -> AsyncCollection:
    if db_name in internals.dbs:
        return internals.dbs[db_name][collection_name]
    else:
        logging.error('Cannot return collection when db is not connected')
        raise Exception('Cannot return collection when db is not connected')

def setup_db(db_name: str | None = None) -> None:
    connect_client()
    connect_db(db_name or parsed_config.DB_NAME)
