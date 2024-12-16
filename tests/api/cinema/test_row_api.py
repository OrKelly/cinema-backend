import random

from httpx import AsyncClient

from apps.cinema.exceptions.halls import HallNotFoundException
from apps.cinema.exceptions.rows import RowAlreadyExistsException
from apps.cinema.services.rows import BaseRowService
from tests.factories.halls import HallFactory
from tests.factories.row import RowFactory


class TestRowAPI:
    @staticmethod
    def get_create_url(**kwargs):
        return "api/v1/cinema/rows"

    async def test_row_create_with_exist_hall(
        self, client: AsyncClient, container
    ):
        hall = await HallFactory().create()
        payload = {
            "hall_id": hall.id,
            "number": random.randint(1, 10),
        }
        response = await client.post(self.get_create_url(), json=payload)
        assert response.status_code == 200
        row_service = container.resolve(BaseRowService)
        row = await row_service.get_by_id(response.json()["data"]["id"])
        assert row.id == response.json()["data"]["id"]
        for attr, value in payload.items():
            if hasattr(row, attr):
                assert getattr(row, attr) == value

    async def test_row_create_without_existing_hall(
        self, client: AsyncClient, prepare_database
    ):
        payload = {
            "hall_id": random.randint(1, 10),
            "number": random.randint(1, 10),
        }
        response = await client.post(self.get_create_url(), json=payload)
        assert response.status_code == 404
        assert response.json()["message"] == HallNotFoundException().message

    async def test_row_create_with_exist_row_number_in_hall(
        self, client: AsyncClient, faker
    ):
        row = await RowFactory().create()
        payload = {
            "hall_id": row.hall_id,
            "number": row.number,
        }
        response = await client.post(self.get_create_url(), json=payload)
        assert response.status_code == 409
        assert (
            response.json()["message"] == RowAlreadyExistsException().message
        )
