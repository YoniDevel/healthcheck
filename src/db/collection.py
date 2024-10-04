import logging
from pydantic import BaseModel
from pymongo import ReturnDocument
from typing import Generic, Optional, Type, TypeVar
from pymongo.results import InsertOneResult, DeleteResult
from pymongo.asynchronous.collection import AsyncCollection

from src.db.connection import get_collection

T = TypeVar('T', bound=BaseModel)

class CollectionOperations(Generic[T]):
    def __init__(self, cls: Type[T], collection_name: str) -> None:
        self.cls = cls
        self.collection_name = collection_name
        self.collection = get_collection(self.collection_name)
               
    async def insert_one(self, document: T) -> InsertOneResult:
        result = await self.collection.insert_one(document.model_dump())
        return result.inserted_id
        
    async def find_one(self, filter: dict) -> Optional[T]:
        return await self.collection.find_one(filter)
    
    async def find(self, filter: dict, options: dict) -> list[T]:
        documents = await self.collection.find(filter, **options).to_list()
        return list(map(lambda document: self.cls(**document), documents))
    
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
