import random

import pytest
from httpx import AsyncClient

from apps.cinema.models.rows import Row
from apps.cinema.models.halls import Hall
from apps.cinema.services.rows import ORMRowService, BaseRowService
from apps.cinema.repositories.halls import ORMHallRepository
from tests.factories.user import UserFactory


class TestRowAPI:
    @staticmethod
    def get_create_url(**kwargs):
        return "api/v1/cinema/rows"

    @pytest.mark.parametrize(("payload",), [{"hall_id": 1, "number": 1}])
    async def test_row_create_with_exist_hall(self, client: AsyncClient, payload, container, prepare_database):
        # payload = {
        #     "hall_id": random.randint(1, 10),
        #     "number": random.randint(1, 10),
        # }
        hall_response = await container.resolve(ORMHallRepository)
        response = await client.post(self.get_create_url(), json=payload)
        assert response.status_code == 200
        row_service = container.resolve(BaseRowService)
        row = await row_service.get_by_id(response.json()["data"]["id"])
        assert row.id == response.json()["data"]["id"]
        for attr, value in payload.items():
            if hasattr(row, attr):
                assert getattr(row, attr) == value
