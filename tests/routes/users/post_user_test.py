import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.app import create_app
from src.models.user import User
from src.db.connection import setup_db
from tests.testData.users import create_random_user, create_random_user_to_insert, edit_user_for_assertions
from src.db.collections.users import UsersCollection

app = create_app()
client = TestClient(app)


@pytest.fixture(scope='module', autouse=True)
def setup_users_collection() -> UsersCollection:
    setup_db()
    return UsersCollection()

@pytest.fixture(scope='function', autouse=True)
async def clean_db() -> None:
    await UsersCollection().delete_many({})
    
@pytest.mark.asyncio
async def test_post_user_regular_case() -> None:
    user = create_random_user_to_insert()
    
    response = client.post('/users', json=[user])
    
    inserted_user = await UsersCollection().find({}, {"projection": {"createdAt": 0, "updatedAt": 0}})
    user_for_comparison = edit_user_for_assertions(user)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert inserted_user == [user_for_comparison]
    