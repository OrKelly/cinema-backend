from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from faker import Faker

from apps.films.models.films import Film
from core.enums.films import AgeRatingEnum, FilmStatusEnum
from tests.factories.base import BaseFactory, BaseFakeSchema, SubFactory

from .halls import HallFactory

fake = Faker(locale="ru_RU")


@dataclass
class FilmCreate(BaseFakeSchema):
    cinemahall_id = SubFactory(factory=HallFactory)
    title: str = fake.word
    description: str = fake.text
    poster: str = fake.url
    age_rating: Enum = fake.enum(AgeRatingEnum)
    duration: float = fake.pyfloat
    status: Enum = fake.enum(FilmStatusEnum)
    date_rent_start: datetime = fake.date
    date_rent_end: datetime = fake.date

    class Meta:
        model = Film


class FilmFactory(BaseFactory[Film, FilmCreate]):
    model_class = Film
    schema = FilmCreate
