import pytest
from fastapi import status
from typing import Any, AsyncGenerator
from httpx import ASGITransport, AsyncClient

from src.models.user import User
from src.app import app
from src.db.collections.users import UsersCollection
from src.db.connection import disconnect_mongo, connect_mongo
from tests.testData.users import create_random_user_dict_to_insert, create_random_user_model_to_insert, edit_user_for_assertions

client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

@pytest.fixture(scope='function', autouse=True)
async def setup_and_teardown() -> AsyncGenerator[None, Any]:
    connect_mongo()
    yield
    await UsersCollection().delete_many({})
    disconnect_mongo()

async def test_get_by_id_regular_case() -> None:
    user = create_random_user_model_to_insert()
    await UsersCollection().insert_one(user)
    
    response = await client.get(f'/users/{user.id}')
    
    assert response.status_code == status.HTTP_200_OK
    assert User(**response.json()).model_dump(exclude={'createdAt', 'updatedAt'}) == user.model_dump(exclude_defaults=True)

async def test_get_by_id_not_found() -> None:
    dummy_users = [create_random_user_model_to_insert() for _ in range(10)]
    non_existent_id = 'nonexistentid'
    await UsersCollection().insert_many(dummy_users)
    
    response = await client.get(f'/users/{non_existent_id}')
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['message'] == f'Cannot find user with id {non_existent_id}'
