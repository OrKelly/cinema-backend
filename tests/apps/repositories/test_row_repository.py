from typing import cast

from apps.cinema.models import Row
from apps.cinema.repositories.rows import (
    ORMRowRepository,
)
from core.generics import ModelType
from tests.factories.row import RowFactory


class TestRowRepository:
    async def test_create_hall(self):
        attrs = await RowFactory().row()
        repository = ORMRowRepository(model_class=cast(ModelType, Row))
        row = await repository.create(attributes=attrs)
        assert row
        assert await repository.get_by(field="id", value=row.id, unique=True)
        for attr, value in attrs.items():
            if hasattr(row, attr):
                assert getattr(row, attr) == value
