import logging
from pymongo import ReturnDocument
from typing import Generic, Mapping, Optional, TypeVar
from pymongo.results import InsertOneResult, DeleteResult
from pymongo.asynchronous.collection import AsyncCollection

from src.db.connection import internals

T = TypeVar('T', bound=Mapping[str, None])

class CollectionOperations(Generic[T]):
    def __init__(self, collection_name: str) -> None:
        self.collection_name = collection_name
        if internals.db is not None:
            self.collection: AsyncCollection[T] = internals.db[collection_name]
        else:
            logging.error('Cannot return collection when db is not connected')
            raise Exception('Cannot return collection when db is not connected')
               
    async def insert_one(self, document: T) -> InsertOneResult:
        result = await self.collection.insert_one(document)
        return result.inserted_id
        
    async def find_one(self, filter: dict) -> Optional[T]:
        return await self.collection.find_one(filter)
    
    async def find(self, filter: dict, options: dict) -> list[T]:
        cursor = self.collection.find(filter, **options)
        return await cursor.to_list()
    
    async def update_one(self, filter: dict, update: dict, options: dict) -> T:
        result = await self.collection.find_one_and_update(
            filter, 
            update, 
            return_document=ReturnDocument.AFTER,
            **options
        )
        return result
        
    async def delete_one(self, filter: dict) -> DeleteResult:
        result = await self.collection.delete_one(filter)
        return result
