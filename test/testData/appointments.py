import random
from faker import Faker

from models.appointment import Appointment, Visit

faker = Faker()

def create_random_appointment() -> Appointment:
    date_of_last_visit = faker.date_this_year()
    return Appointment(**{
        'name': random.choice(['skin', 'eyes', 'dentist', 'chiropractor']),
        'frequency': faker.random_int(min=30, max=365),
        'lastVisit': Visit(**{
            'date': date_of_last_visit,
            'city': faker.city()
        }),
        'nextVisit': Visit(**{
            'date': faker.date_between(start_date=date_of_last_visit, end_date=faker.future_date()),
            'city': faker.city()
        })
    })
