import random

import pytest
from faker import Faker
from httpx import AsyncClient

from apps.cinema.exceptions.halls import (
    HallAlreadyExists,
    HallNotFoundException,
)
from apps.cinema.services.halls import BaseHallService
from apps.cinema.services.rows import BaseRowService
from core.containers import get_container
from tests.factories.halls import HallFactory
from tests.factories.row import RowFactory

fake = Faker(locale="ru_RU")
hall_service: BaseHallService = get_container().resolve(BaseHallService)


class TestHallApi:
    @staticmethod
    def get_list_url(*args, **kwargs):
        return "/".join(("api/v1/cinema/halls", *map(str, args)))

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

        response = await client.get(self.get_list_url(hall.id))

        response_json = response.json()["data"]
        assert response.status_code == 200
        assert hall.id == response_json["id"]
        assert hall.title == response_json["title"]
        assert hall.description == response_json["description"]
        assert len(response_json["rows"]) == rows_amount
        assert response_json["rows"][0]["capacity"] == rows_capacity
        assert len(response_json["rows"][0]["places"]) == rows_capacity

    async def test_hall_get_with_rows_and_places_not_exist(
        self, prepare_database, client: AsyncClient, container, faker
    ):
        response = await client.get(
            self.get_list_url(faker.pyint(max_value=30))
        )
        response_json = response.json()

        assert response.status_code == 404
        assert response_json["message"] == HallNotFoundException().message

    @pytest.mark.parametrize(
        ("payload", "flag"),
        [
            (
                {
                    "title": fake.pystr(min_chars=1, max_chars=45),
                    "description": fake.pystr(),
                },
                "change_all",
            ),
            ({"description": fake.pystr()}, "change_only_description"),
            (
                {"title": fake.pystr(min_chars=1, max_chars=45)},
                "change_only_title",
            ),
        ],
    )
    async def test_update_hall(self, payload, flag, client: AsyncClient):
        hall = await HallFactory().create()
        initial_hall_title = hall.title
        initial_hall_description = hall.description
        response = await client.patch(self.get_list_url(hall.id), json=payload)
        response_json = response.json()["data"]
        assert response.status_code == 200
        if flag == "change_all":
            assert initial_hall_title != response_json["title"]
            assert initial_hall_description != response_json["description"]
        if flag == "change_only_description":
            assert initial_hall_title == response_json["title"]
            assert initial_hall_description != response_json["description"]
        if flag == "change_only_title":
            assert initial_hall_title != response_json["title"]
            assert initial_hall_description == response_json["description"]

    async def test_update_hall_with_exist_title(
        self, client: AsyncClient, faker
    ):
        first_hall = await HallFactory().create()
        second_hall = await HallFactory().create()
        payload = {
            "title": first_hall.title,
            "description": faker.pystr(),
        }
        response = await client.patch(
            self.get_list_url(second_hall.id), json=payload
        )
        response_json = response.json()
        assert response.status_code == 409
        assert response_json["message"] == HallAlreadyExists().message

    async def test_update_hall_with_invalid_length_title(
        self, client: AsyncClient
    ):
        hall = await HallFactory().create()
        payload = await HallFactory().row()
        payload["title"] = fake.pystr(min_chars=50, max_chars=50)
        response = await client.patch(self.get_list_url(hall.id), json=payload)
        assert response.status_code == 422
