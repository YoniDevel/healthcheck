import pytest
from fastapi import status
from typing import Any, AsyncGenerator
from httpx import ASGITransport, AsyncClient

from src.app import app
from src.db.collections.users import UsersCollection
from src.db.connection import disconnect_mongo, setup_db
from tests.testData.users import create_random_user_dict_to_insert, edit_user_for_assertions

client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

@pytest.fixture(scope='function', autouse=True)
async def setup_and_teardown() -> AsyncGenerator[None, Any]:
    setup_db()
    yield
    await UsersCollection().delete_many({})
    disconnect_mongo()
   
@pytest.mark.asyncio
async def test_post_user_regular_case() -> None:
    user = create_random_user_dict_to_insert()
    
    response = await client.post('/users', json=[user])
    
    inserted_user = await UsersCollection().find({}, {"projection": {"createdAt": 0, "updatedAt": 0}})
    user_for_comparison = edit_user_for_assertions(user)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert inserted_user == [user_for_comparison]

@pytest.mark.asyncio
async def test_post_user_regular_case_multiple_users() -> None:
    users = [create_random_user_dict_to_insert() for _ in range(10)]
    
    response = await client.post('/users', json=users)
        
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == len(users)

@pytest.mark.asyncio
async def test_post_user_bad_user_inserted() -> None:
    bad_user = create_random_user_dict_to_insert()
    del bad_user['firstName']
    
    response = await client.post('/users', json=[bad_user])
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'firstName' in response.json()['detail'][0]['loc']
