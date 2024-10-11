from fastapi import status
from fastapi.testclient import TestClient

from src.app import create_app

app = create_app()
client = TestClient(app)

def test_health_route() -> None:
    response = client.get('/health')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "I am alive and kicking"
