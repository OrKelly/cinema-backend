from dataclasses import dataclass

from faker import Faker

from apps.cinema.models.places import Place
from tests.factories.base import BaseFactory, BaseFakeSchema, SubFactory

from .row import RowFactory

fake = Faker(locale="ru_RU")


@dataclass
class PlaceCreate(BaseFakeSchema):
    number = fake.pyint
    row_id = SubFactory(factory=RowFactory)

    class Meta:
        model = Place


class PlaceFactory(BaseFactory[Place, PlaceCreate]):
    model_class = Place
    schema = PlaceCreate
