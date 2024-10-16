import pytest
from fastapi import status
from typing import Any, AsyncGenerator
from httpx import ASGITransport, AsyncClient

from src.models.user import User
from src.app import app
from src.db.collections.users import UsersCollection
from src.db.connection import disconnect_mongo, setup_db
from tests.testData.appointments import create_random_appointment
from tests.testData.users import create_random_user_dict_to_insert, create_random_user_model_to_insert, edit_user_for_assertions

client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

@pytest.fixture(scope='function', autouse=True)
async def setup_and_teardown() -> AsyncGenerator[None, Any]:
    setup_db()
    yield
    await UsersCollection().delete_many({})
    disconnect_mongo()
    
async def test_put_appointment_regular_case() -> None:
    user = create_random_user_model_to_insert()
    appointment = create_random_appointment()
    await UsersCollection().insert_one(user)
    
    response = await client.put(f'/users/{user.id}/appointment', json=appointment)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['appointments'][-1] == appointment
    
async def test_put_appointment_first_appointment() -> None:
    user = create_random_user_model_to_insert()
    user.appointments = []
    appointment = create_random_appointment()
    await UsersCollection().insert_one(user)
    
    response = await client.put(f'/users/{user.id}/appointment', json=appointment)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['appointments'][0] == appointment    


async def test_put_appointment_user_not_found() -> None:
    fake_id = 'fake'
    appointment = create_random_appointment()
    
    response = await client.put(f'/users/{fake_id}/appointment', json=appointment)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['message'] == f'Cannot find user with id {fake_id}'