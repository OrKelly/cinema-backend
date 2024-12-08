from faker import Faker
from pydantic import BaseModel, Field

from apps.cinema.models.halls import Hall
from tests.factories.base import BaseFactory

fake = Faker(locale='ru_RU')


class HallCreate(BaseModel):
    title: str = Field(default_factory=fake.company)
    description: str = Field(default_factory=fake.text)


class HallFactory(BaseFactory[Hall, HallCreate]):
    model_class = Hall
    schema = HallCreate

