from apps.cinema.services.rows import BaseRowService
from core.containers import get_container
from tests.factories.halls import HallFactory
from tests.factories.row import RowFactory


class TestRowServices:
    row_service = get_container().resolve(BaseRowService)

    async def test_create(self):
        attrs = await RowFactory().row()
        row = await self.row_service.create(attributes=attrs)
        assert row
        for attr, value in attrs.items():
            if hasattr(row, attr):
                assert getattr(row, attr) == value

    async def test_get_all(self, prepare_database):
        await RowFactory().create_batch(10)
        all_rows = await self.row_service.get_all()
        assert len(all_rows) == 10

    async def test_get_by_id(self):
        await RowFactory().create_batch(10)
        row = await self.row_service.get_by_id(id_=9)
        assert row
        assert row.id == 9

    async def test_get_by_hall(self, prepare_database):
        await HallFactory().create_batch(10)
        await RowFactory(hall_id=9).create_batch(5)
        all_rows_need_hall = await self.row_service.get_by_hall(hall_id=9)
        assert len(all_rows_need_hall) == 5

    async def test_get_by_filter(self, prepare_database):
        await RowFactory(number=9).create_batch(5)
        all_rows_need_hall = await self.row_service.get_by_filter(
            filter_params={"number": 9}
        )
        assert len(all_rows_need_hall) == 5
