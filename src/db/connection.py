import logging
from typing import TypeVar, Type
import motor
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from typing import Optional
import motor.motor_asyncio
from pydantic import BaseModel

from config import parsed_config

class DBInternals(BaseModel):
    client: Optional[AsyncIOMotorClient]
    db: Optional[AsyncIOMotorDatabase]

T = TypeVar('T')

internals = DBInternals(
    client = None,
    db = None
)

def connect_client() -> None:
    if not internals.client:
        client = AsyncIOMotorClient(str(parsed_config.MONGO_URI))
        internals.client = client

def connect_db() -> None:
    if not internals.client:
        logging.error('Cannot connect to db because client does not exist')
        raise Exception('Cannot connect to db because client does not exist')
    internals.db = internals.client[parsed_config.DB_NAME]

def setup_db() -> None:
    connect_client()
    connect_db()

def get_collection(collection_name: str) -> AsyncIOMotorCollection:
    if internals.db is not None:
        return internals.db[collection_name]
    else:
        logging.error('Cannot return collection when db is not connected')
        raise Exception('Cannot return collection when db is not connected')
