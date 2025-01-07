import random

from httpx import AsyncClient

from apps.cinema.exceptions.halls import HallNotFoundException
from apps.cinema.exceptions.rows import RowAlreadyExistsException
from apps.cinema.services.places import BasePlaceService
from apps.cinema.services.rows import BaseRowService
from tests.factories.row import RowFactory


class TestRowAPI:
    @staticmethod
    def get_list_url(**kwargs):
        return "api/v1/cinema/rows"

    async def test_row_create_with_exist_hall(
        self, client: AsyncClient, container
    ):
        payload = await RowFactory().row()
        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 200
        row_service = container.resolve(BaseRowService)
        place_service = container.resolve(BasePlaceService)
        row = await row_service.get_by_id(response.json()["data"]["id"])
        current_row_places = await place_service.get_by_row(row_id=row.id)
        assert row.id == response.json()["data"]["id"]
        assert len(current_row_places) == payload["capacity"]
        for attr, value in payload.items():
            if hasattr(row, attr):
                assert getattr(row, attr) == value

    async def test_row_create_without_existing_hall(
        self, client: AsyncClient, prepare_database
    ):
        payload = await RowFactory().row()
        payload.update({"hall_id": random.randint(2, 10)})
        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 404
        assert response.json()["message"] == HallNotFoundException().message

    async def test_row_create_with_exist_row_number_in_hall(
        self, client: AsyncClient
    ):
        row = await RowFactory().create()
        payload = {
            "hall_id": row.hall_id,
            "number": row.number,
            "capacity": row.capacity,
        }
        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 409
        assert (
            response.json()["message"] == RowAlreadyExistsException().message
        )

    async def test_row_get_with_places(self, client: AsyncClient, container):
        payload = await RowFactory().row()
        row_service = container.resolve(BaseRowService)
        row = await row_service.create(payload)
        response = await client.get(
            "/".join((self.get_list_url(), str(row.id)))
        )
        assert response.status_code == 200
        response_json = response.json()
        assert row.id == response_json["id"]
        assert row.number == response_json["number"]
        assert row.capacity == response_json["capacity"]
        assert row.capacity == len(response_json["places"])
        for number, place in enumerate(response_json["places"], start=1):
            assert place["id"]
            assert place["number"] == number
