import pytest
from fastapi import status
from typing import Any, AsyncGenerator
from httpx import ASGITransport, AsyncClient

from src.app import app
from src.models.user import User
from src.db.collections.users import UsersCollection
from src.db.connection import disconnect_mongo, connect_mongo
from tests.testData.users import create_random_user_model_to_insert

client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

@pytest.fixture(scope='function', autouse=True)
async def setup_and_teardown() -> AsyncGenerator[None, Any]:
    connect_mongo()
    yield
    await UsersCollection().delete_many({})
    disconnect_mongo()

async def test_get_all_users_empty_db() -> None:
    response = await client.get('/users')
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    
async def test_get_all_users_regular_case() -> None:
    users_to_insert = [create_random_user_model_to_insert() for _ in range(10)]
    await UsersCollection().insert_many(users_to_insert)
    
    response = await client.get('/users')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(users_to_insert)
