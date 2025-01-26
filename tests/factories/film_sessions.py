from dataclasses import dataclass
from datetime import datetime

from faker import Faker

from apps.films.models import FilmSession
from tests.factories.base import BaseFactory, BaseFakeSchema, SubFactory
from tests.factories.films import FilmFactory

fake = Faker(locale="ru_RU")


@dataclass
class FilmSessionCreate(BaseFakeSchema):
    film_id = SubFactory(factory=FilmFactory)
    date_time: datetime = fake.date_time
    price: float = fake.pyfloat

    class Meta:
        model = FilmSession


class FilmSessionFactory(BaseFactory[FilmSession, FilmSessionCreate]):
    model_class = FilmSession
    schema = FilmSessionCreate
