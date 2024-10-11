import random
from faker import Faker

from models.user import User
from utils.control_digit import calc_control_digit
from testData.appointments import create_random_appointment

faker = Faker()

def create_random_valid_id() -> str:
    id_without_control_digit = str(random.randint(0, 9)) + str(random.randint(1, 987654321))
    return id_without_control_digit + str(calc_control_digit(id_without_control_digit))

def create_random_user() -> User:
    return User(**{
        '_id': create_random_valid_id(),
        'firstName': faker.first_name(),
        'lastName': faker.last_name(),
        'dateOfBirth': faker.date_of_birth(minimum_age=1, maximum_age=120),
        'email': faker.email(),
        'clalitUserCode': faker.user_name(),
        'clalitPassword': faker.password(),
        'appointments': [create_random_appointment()] * 2
    })
