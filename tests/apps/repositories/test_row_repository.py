from apps.cinema.repositories.rows import BaseRowRepository
from core.containers import get_container
from tests.factories.row import RowFactory


class TestRowRepository:
    row_repository = get_container().resolve(BaseRowRepository)

    async def test_create(self):
        attrs = await RowFactory().row()
        row = await self.row_repository.create(attributes=attrs)
        assert row
        for attr, value in attrs.items():
            if hasattr(row, attr):
                assert getattr(row, attr) == value
