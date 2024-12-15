from faker import Faker
from pydantic import BaseModel, Field

from apps.cinema.models.rows import Row
from tests.factories.base import BaseFactory, SubFactory

from .halls import HallFactory

fake = Faker(locale="ru_RU")


class RowCreate(BaseModel):
    number: int = Field(default_factory=fake.pyint)


class RowFactory(BaseFactory[Row, RowCreate]):
    model_class = Row
    schema = RowCreate
    sub_factories = [SubFactory(factory=HallFactory, foreign_key="hall_id")]
