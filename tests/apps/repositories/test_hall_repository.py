from typing import cast

from apps.cinema.models import Hall
from apps.cinema.repositories.halls import (
    ORMHallRepository,
)
from core.generics import ModelType
from tests.factories.halls import HallFactory


class TestHallRepository:
    async def test_create_hall(self):
        attrs = await HallFactory()._get_instance_data()
        repository = ORMHallRepository(model_class=cast(ModelType, Hall))
        hall = await repository.create(attributes=attrs)
        assert hall
        assert await repository.get_by(field="id", value=hall.id, unique=True)
        for attr, value in attrs.items():
            if hasattr(hall, attr):
                assert getattr(hall, attr) == value
