from dataclasses import dataclass
from datetime import datetime

from faker import Faker

from apps.films.models import FilmSession
from tests.factories.base import BaseFactory, BaseFakeSchema, SubFactory
from tests.factories.films import FilmFactory

from .halls import HallFactory

fake = Faker(locale="ru_RU")


@dataclass
class FilmSessionCreate(BaseFakeSchema):
    film_id = SubFactory(factory=FilmFactory)
    hall_id = SubFactory(factory=HallFactory)
    date_time: datetime = fake.date_time
    price: float = fake.pydecimal(left_digits=8, right_digits=2)

    class Meta:
        model = FilmSession


class FilmSessionFactory(BaseFactory[FilmSession, FilmSessionCreate]):
    model_class = FilmSession
    schema = FilmSessionCreate
