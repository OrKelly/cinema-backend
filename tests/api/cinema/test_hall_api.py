import random

from httpx import AsyncClient

from apps.cinema.services.halls import BaseHallService
from apps.cinema.services.rows import BaseRowService
from core.containers import get_container
from tests.factories.halls import HallFactory
from tests.factories.row import RowFactory

hall_service: BaseHallService = get_container().resolve(BaseHallService)


class TestHallApi:
    @staticmethod
    def get_list_url(**kwargs):
        return "api/v1/cinema/halls"

    async def test_create_hall(
        self, client: AsyncClient, faker, prepare_database
    ):
        payload = {
            "title": faker.company(),
            "description": faker.text(),
        }
        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 200
        hall = await hall_service.get_by_id(response.json()["data"]["id"])
        assert hall.id == response.json()["data"]["id"]
        for attr, value in payload.items():
            if hasattr(hall, attr):
                assert getattr(hall, attr) == value

    async def test_create_hall_with_exist_title(
        self, client: AsyncClient, faker
    ):
        hall = await HallFactory().create()
        payload = {
            "title": hall.title,
            "description": faker.text(),
        }
        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 409
        hall = await hall_service.get_by_filter(
            filter_params={"description": payload["description"]}
        )
        assert not hall

    async def test_hall_get_with_rows_and_places(
        self, client: AsyncClient, container
    ):
        hall = await HallFactory().create()
        row_service = container.resolve(BaseRowService)
        payload = await RowFactory().row()
        payload["hall_id"] = hall.id
        rows_capacity = payload["capacity"]
        rows_amount = random.randint(2, 10)
        for _i in range(rows_amount):
            await row_service.create(payload)

        response = await client.get(
            "/".join((self.get_list_url(), str(hall.id)))
        )

        response_json = response.json()["data"]
        assert response.status_code == 200
        assert hall.id == response_json["id"]
        assert hall.title == response_json["title"]
        assert hall.description == response_json["description"]
        assert len(response_json["rows"]) == rows_amount
        assert response_json["rows"][0]["capacity"] == rows_capacity
        assert len(response_json["rows"][0]["places"]) == rows_capacity

    async def test_update_hall(self, client: AsyncClient):
        hall = await HallFactory().create()
        payload = await HallFactory().row()
        initial_hall_title = hall.title
        initial_hall_description = hall.description
        response = await client.put(
            "/".join((self.get_list_url(), str(hall.id))), json=payload
        )
        response_json = response.json()["data"]
        assert response.status_code == 200
        assert initial_hall_title != response_json["title"]
        assert initial_hall_description != response_json["description"]

    async def test_update_hall_with_invalid_length_title(
        self, client: AsyncClient
    ):
        hall = await HallFactory().create()
        payload = await HallFactory().row()
        payload["title"] = payload.get("title")[0] * 50
        response = await client.put(
            "/".join((self.get_list_url(), str(hall.id))), json=payload
        )
        assert response.status_code == 422
