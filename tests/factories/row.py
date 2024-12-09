from random import randint

from pydantic import BaseModel, Field

from apps.cinema.models import Row
from tests.factories.base import BaseFactory


def get_random_number():
    return randint(1, 10)


class RowCreate(BaseModel):
    hall_id: int = Field(default_factory=get_random_number)
    number: int = Field(default_factory=get_random_number)


class RowFactory(BaseFactory[Row, RowCreate]):
    model_class: Row
    schema: RowCreate

    async def _get_instance_data(self) -> dict:
        instance_data = await super()._get_instance_data()
        return instance_data
