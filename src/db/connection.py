import logging
from pydantic import BaseModel
from pymongo import AsyncMongoClient
from typing import Mapping, Optional, TypeVar
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.collection import AsyncCollection

from config import parsed_config

class DBInternals(BaseModel):
    client: Optional[AsyncMongoClient]
    db: Optional[AsyncDatabase]

internals = DBInternals(
    client = None,
    db = None
)

T = TypeVar('T', bound=Mapping[str, None])

def connect_client() -> None:
    if not internals.client:
        client = AsyncMongoClient(str(parsed_config.MONGO_URI))
        internals.client = client

def connect_db() -> None:
    if not internals.client:
        logging.error('Cannot connect to db because client does not exist')
        raise Exception('Cannot connect to db because client does not exist')
    internals.db = internals.client[parsed_config.DB_NAME]

def get_collection(collection_name: str) -> AsyncCollection:
    if internals.db is not None:
        return internals.db[collection_name]
    else:
        logging.error('Cannot return collection when db is not connected')
        raise Exception('Cannot return collection when db is not connected')

def setup_db() -> None:
    connect_client()
    connect_db()
