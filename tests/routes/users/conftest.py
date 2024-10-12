import pytest
from pytest import Session

from src.db.collections.users import UsersCollection
from src.db.connection import setup_db

@pytest.fixture(scope='session')
def setup_users_collection() -> UsersCollection:
    setup_db()
    return UsersCollection()
