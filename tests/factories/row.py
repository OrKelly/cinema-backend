from dataclasses import dataclass

from faker import Faker

from apps.cinema.models.rows import Row
from tests.factories.base import BaseFactory, BaseFakeSchema, SubFactory

from .halls import HallFactory

fake = Faker(locale="ru_RU")
Faker.seed(4321)


@dataclass
class RowCreate(BaseFakeSchema):
    number = fake.pyint
    hall_id = SubFactory(factory=HallFactory)
    capacity = fake.pyint(min_value=10, max_value=30)

    class Meta:
        model = Row


class RowFactory(BaseFactory[Row, RowCreate]):
    model_class = Row
    schema = RowCreate
