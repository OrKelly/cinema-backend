import pytest
from httpx import AsyncClient

from apps.cinema.services.halls import BaseHallService
from tests.factories.halls import HallFactory


class TestHallApi:
    @staticmethod
    def get_register_url(**kwargs):
        return "api/v1/cinema/halls"
    
    async def test_create_hall(self, client: AsyncClient, faker, container):
        payload = {
            "title": faker.company(),
            "description": faker.text(),
        }
        response = await client.post(self.get_register_url(), json=payload)
        assert response.status_code == 200
        hall_service = container.resolve(BaseHallService)
        hall = await hall_service.get_by_id(response.json()["data"]["id"])
        assert hall.id == response.json()["data"]["id"]
        for attr, value in payload.items():
            if hasattr(hall, attr):
                assert getattr(hall, attr) == value
    
    async def test_create_hall_with_exist_title(
            self, client: AsyncClient, faker, container
    ):
        hall = await HallFactory().create()
        payload = {
            "title": hall.title,
            "description": faker.text(),
        }
        response = await client.post(self.get_register_url(), json=payload)
        assert response.status_code == 409
        hall_service = container.resolve(BaseHallService)
        hall = await hall_service.get_by_filter(
            field="description", value=payload["description"]
        )
        assert not hall



