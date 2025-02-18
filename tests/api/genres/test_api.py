import pytest
from faker import Faker

from apps.films.services.genres import BaseGenreService

import pytest
from httpx import AsyncClient

from core.containers import get_container
from tests.factories.genre import GenreFactory


class TestGenreAPI:
    @staticmethod
    def get_genres_url(**kwargs):
        return "api/v1/films/genres"

    @pytest.mark.asyncio
    async def test_get_genres(self, client: AsyncClient, faker):
        payload = await GenreFactory().row()
        genre_service = get_container().resolve(BaseGenreService)
        genre = await genre_service.create(payload)

        response = await client.get("/" + self.get_genres_url())
        response_json = response.json()["data"]
        assert response.status_code == 200
        assert genre.id == response_json[0]['id']
        assert genre.title == response_json[0]['title']
