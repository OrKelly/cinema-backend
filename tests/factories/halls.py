from faker import Faker

from apps.cinema.models.halls import Hall
from tests.factories.base import BaseFactory, BaseFakeSchema

fake = Faker(locale="ru_RU")


class HallCreate(BaseFakeSchema):
    title: str = fake.company
    description: str = fake.text

    class Meta:
        model = Hall


class HallFactory(BaseFactory[Hall, HallCreate]):
    model_class = Hall
    schema = HallCreate
