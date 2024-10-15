import pytest
import pytest_asyncio
from fastapi import status
from httpx import ASGITransport, AsyncClient
from typing import Any, AsyncGenerator, Generator

from src.app import create_app
from src.db.connection import disconnect_mongo, setup_db
from src.db.collections.users import UsersCollection
from tests.testData.users import create_random_user_to_insert, edit_user_for_assertions

app = create_app()
client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

@pytest.fixture(scope='session', autouse=True)
async def setup_and_teardown():
    setup_db()
    yield
    disconnect_mongo()

@pytest.fixture(scope='function', autouse=True)
async def setup_users_db():
    yield
    await UsersCollection().delete_many({})
    
@pytest.mark.asyncio
async def test_post_user_regular_case() -> None:
    user = create_random_user_to_insert()
    
    response = await client.post('/users', json=[user])
    
    inserted_user = await UsersCollection().find({}, {"projection": {"createdAt": 0, "updatedAt": 0}})
    user_for_comparison = edit_user_for_assertions(user)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert inserted_user == [user_for_comparison]

@pytest.mark.asyncio
async def test_post_user_bad_user_inserted() -> None:
    bad_user = create_random_user_to_insert()
    del bad_user['firstName']
    
    response = await client.post('/users', json=[bad_user])
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert 'firstName' in response.json()['detail'][0]['loc']
    