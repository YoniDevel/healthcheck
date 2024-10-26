import random
from faker import Faker
from datetime import datetime

from src.models import User
from src.utils import calc_control_digit
from tests.testData.appointments import create_random_appointment

faker = Faker()

def create_random_valid_id() -> str:
    id_without_control_digit = str(random.randint(0, 9)) + str(random.randint(1, 9999999))
    return id_without_control_digit + str(calc_control_digit(id_without_control_digit))

def create_random_user() -> dict:
    return {
        '_id': create_random_valid_id(),
        'firstName': faker.first_name(),
        'lastName': faker.last_name(),
        'dateOfBirth': faker.date_time().isoformat(),
        'email': faker.email(),
        'clalitUserCode': faker.user_name(),
        'clalitPassword': faker.password(),
        'appointments': [create_random_appointment() for _ in range(3)],
        'cityOfResidence': faker.city(),
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }


def create_random_user_dict_to_insert() -> dict:
    user_to_insert = create_random_user()
    del user_to_insert['createdAt']
    del user_to_insert['updatedAt']
    return user_to_insert

def create_random_user_model_to_insert() -> User:
    return User(**create_random_user_dict_to_insert())

def edit_user_for_assertions(user: dict) -> dict:
    user_for_assertion = User(**user).model_dump(by_alias=True)
    del user_for_assertion['createdAt']
    del user_for_assertion['updatedAt']
    return user_for_assertion
    