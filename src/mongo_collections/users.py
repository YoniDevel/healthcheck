from ..models import User
from ..db import CollectionOperations

class UsersCollection(CollectionOperations):
    def __init__(self) -> None:
        super().__init__(User, 'users')
