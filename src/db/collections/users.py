from src.models.user import User
from src.db.collection import CollectionOperations

class UsersCollection(CollectionOperations):
    def __init__(self) -> None:
        super().__init__(User, 'users')
