from faker import Faker
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

from apps.films.models.films import Film
from tests.factories.base import BaseFactory, BaseFakeSchema, SubFactory
from .halls import HallFactory

fake = Faker(locale="ru_RU")


@dataclass
class FilmCreate(BaseFakeSchema):
    cinemahall_id = SubFactory(factory=HallFactory)
    description: str = fake.text
    poster: str = fake.url
    age_rating: Enum = fake.enum
    duration: float = fake.pyfloat
    status: Enum = fake.enum
    date_rent_start: datetime = fake.date
    date_rent_end: datetime = fake.date

    class Meta:
        model = Film


class FilmFactory(BaseFactory[Film, FilmCreate]):
    model_class = Film
    schema = FilmCreate
