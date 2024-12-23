from apps.cinema.services.places import BasePlaceService
from core.containers import get_container
from tests.factories.place import PlaceFactory
from tests.factories.row import RowFactory


class TestPlaceServices:
    place_service = get_container().resolve(BasePlaceService)

    async def test_create(self):
        attrs = await PlaceFactory().row()
        place = await self.place_service.create(attributes=attrs)
        assert place
        for attr, value in attrs.items():
            if hasattr(place, attr):
                assert getattr(place, attr) == value

    async def test_get_all(self, prepare_database):
        await PlaceFactory().create_batch(10)
        all_places = await self.place_service.get_all()
        assert len(all_places) == 10

    async def test_get_by_id(self):
        await PlaceFactory().create_batch(10)
        place = await self.place_service.get_by_id(id_=9)
        assert place
        assert place.id == 9

    async def test_get_by_row(self, prepare_database):
        await RowFactory().create_batch(10)
        await PlaceFactory(row_id=9).create_batch(5)
        all_places_desired_row = await self.place_service.get_by_row(row_id=9)
        assert len(all_places_desired_row) == 5

    async def test_get_by_filter(self, prepare_database):
        await PlaceFactory(number=9).create_batch(5)
        all_places_with_number = await self.place_service.get_by_filter(
            filter_params={"number": 9}
        )
        assert len(all_places_with_number) == 5
