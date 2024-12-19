import random

from httpx import AsyncClient

from apps.cinema.exceptions.places import PlaceAlreadyExistsException
from apps.cinema.exceptions.rows import RowNotFoundException
from apps.cinema.services.places import BasePlaceService
from tests.factories.place import PlaceFactory
from tests.factories.row import RowFactory


class TestPlaceAPI:
    @staticmethod
    def get_list_url(**kwargs):
        return "api/v1/cinema/places"

    async def test_place_create_with_exist_row(
        self, client: AsyncClient, container
    ):
        row = await RowFactory().create()
        payload = {
            "row_id": row.id,
            "number": random.randint(1, 10),
        }
        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 200
        place_service = container.resolve(BasePlaceService)
        place = await place_service.get_by_id(response.json()["data"]["id"])
        assert place.id == response.json()["data"]["id"]
        for attr, value in payload.items():
            if hasattr(place, attr):
                assert getattr(place, attr) == value

    async def test_place_create_without_existing_row(
        self, client: AsyncClient, prepare_database
    ):
        payload = {
            "row_id": random.randint(1, 10),
            "number": random.randint(1, 10),
        }
        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 404
        assert response.json()["message"] == RowNotFoundException().message

    async def test_row_create_with_exist_place_number_in_row(
        self, client: AsyncClient
    ):
        place = await PlaceFactory().create()
        payload = {
            "row_id": place.row_id,
            "number": place.number,
        }
        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 409
        assert (
            response.json()["message"] == PlaceAlreadyExistsException().message
        )
