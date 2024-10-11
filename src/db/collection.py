from abc import ABC
from datetime import datetime
from pydantic import BaseModel
from pymongo import ReturnDocument
from pymongo.results import DeleteResult
from typing import Generic, Optional, Type, TypeVar

from src.db.connection import get_collection

T = TypeVar('T', bound=BaseModel)

class CollectionOperations(ABC, Generic[T]):
    def __init__(self, cls: Type[T], collection_name: str) -> None:
        self.cls = cls
        self.collection_name = collection_name
        self.collection = get_collection(self.collection_name)
               
    async def insert_one(self, document: T) -> str:
        result = await self.collection.insert_one({
            **document.model_dump(),
            'createdAt': datetime.now()
        })
        return result.inserted_id
    
    async def insert_many(self, documents: list[T]) -> list[str]:
        inserted_ids = [await self.insert_one(doc) for doc in documents]
        return inserted_ids
    
    async def find_one(self, filter: dict) -> Optional[T]:
        return await self.collection.find_one(filter)
    
    async def find(self, filter: dict, options: dict = {}) -> list[T]:
        documents = await self.collection.find(filter, **options).to_list()
        return list(map(lambda document: self.cls(**document), documents))
    
    async def update_one(self, filter: dict, update: dict, options: dict = {}) -> T:
        result = await self.collection.find_one_and_update(
            filter, 
            {
                **update,
                'updatedAt': datetime.now()
            },
            return_document=ReturnDocument.AFTER,
            **options or {}
        )
        return result
        
    async def delete_one(self, filter: dict) -> DeleteResult:
        result = await self.collection.delete_one(filter)
        return result
