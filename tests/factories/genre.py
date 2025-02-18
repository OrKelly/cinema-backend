from dataclasses import dataclass

from faker import Faker

from apps.films.models.genres import Genre
from tests.factories.base import BaseFactory, BaseFakeSchema

fake = Faker(locale="ru_RU")


@dataclass
class GenreCreate(BaseFakeSchema):
    title: str = fake.word

    class Meta:
        model = Genre


class GenreFactory(BaseFactory[Genre, GenreCreate]):
    model_class = Genre
    schema = GenreCreate
