import random
from faker import Faker

from src.models.appointment import Appointment

faker = Faker()

def create_random_appointment() -> dict:
    date_of_last_visit = faker.date_time_this_year()
    return {
        'name': random.choice(['skin', 'eyes', 'dentist', 'chiropractor']),
        'frequency': faker.random_int(min=30, max=365),
        'lastVisit': {
            'date': date_of_last_visit.isoformat(),
            'city': faker.city()
        },
        'nextVisit': {
            'date': faker.date_time_between(start_date=date_of_last_visit, end_date=faker.future_date()).isoformat(),
            'city': faker.city()
        }
    }
