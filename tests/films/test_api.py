from datetime import datetime, UTC, timedelta
import pytest
from httpx import AsyncClient

from tests.factories.halls import HallFactory
from core.enums.films import FilmStatusEnum, AgeRatingEnum
from apps.films.services.films import BaseFilmService


class TestFilmAPI:
    @staticmethod
    def get_list_url(**kwargs):
        return "api/v1/films/add"

    @pytest.mark.ayncio
    async def test_create_film(
        self, client: AsyncClient, faker, container
    ):
        hall = await HallFactory().create()
        date_rent_start = datetime.now(UTC) - timedelta(4)
        payload = {
            "cinemahall_id": hall.id,
            "description": faker.text(),
            "poster": faker.url(),
            "age_rating": faker.enum(AgeRatingEnum),
            "duration": faker.pyfloat(),
            "status": faker(FilmStatusEnum),
            "date_rent_start": date_rent_start,
            "date_rent_end": date_rent_start + timedelta(1),
        }

        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 200
        film_service = container.resolve(BaseFilmService)
        film = await film_service.get_by_id(response.json()["data"]["id"])
        assert film.id == response.json()["data"]["id"]
        for attr, value in payload.items():
            if hasattr(film, attr):
                assert getattr(hall, attr) == value

    async def test_create_film_with_wrong_startdate(
            self, client: AsyncClient, faker, container
    ):
        hall = await HallFactory().create()
        date_rent_start = datetime.now(UTC) + timedelta(1)
        payload = {
            "cinemahall_id": hall.id,
            "description": faker.text(),
            "poster": faker.url(),
            "age_rating": faker.enum(AgeRatingEnum),
            "duration": faker.pyfloat(),
            "status": faker(FilmStatusEnum),
            "date_rent_start": date_rent_start,
            "date_rent_end": date_rent_start + timedelta(1),
        }
        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 409
        film_service = container.resolve(BaseFilmService)
        films = await film_service.get_all()
        assert not films

    async def test_create_film_with_wrong_enddate(
            self, client: AsyncClient, faker, container
    ):
        hall = await HallFactory().create()
        date_rent_start = datetime.now(UTC) - timedelta(4)
        payload = {
            "cinemahall_id": hall.id,
            "description": faker.text(),
            "poster": faker.url(),
            "age_rating": faker.enum(AgeRatingEnum),
            "duration": faker.pyfloat(),
            "status": faker(FilmStatusEnum),
            "date_rent_start": date_rent_start,
            "date_rent_end": date_rent_start - timedelta(1),
        }
        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 409
        film_service = container.resolve(BaseFilmService)
        films = await film_service.get_all()
        assert not films
