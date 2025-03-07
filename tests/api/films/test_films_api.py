from datetime import UTC, datetime, timedelta
from enum import Enum

import pytest
from httpx import AsyncClient

from apps.films.exceptions.films import FilmNotFoundException
from apps.films.services.films import BaseFilmService
from tests.factories.film_sessions import FilmSessionFactory
from tests.factories.films import FilmFactory
from tests.factories.genres import GenreFactory
from tests.factories.halls import HallFactory


class TestFilmAPI:
    @staticmethod
    def get_list_url(*args, **kwargs):
        return "api/v1/films/" + "/".join(map(str, args))

    @staticmethod
    async def generate_payload(date_rent_start, date_rent_end):
        hall = await HallFactory().create()
        film = await FilmFactory().row()
        return {
            "cinemahall_id": hall.id,
            "title": film["title"],
            "description": film["description"],
            "age_rating": film["age_rating"].value,
            "duration": film["duration"],
            "status": film["status"].value,
            "date_rent_start": date_rent_start.isoformat(),
            "date_rent_end": date_rent_end.isoformat(),
        }

    @pytest.mark.asyncio
    async def test_create_film(
        self,
        client: AsyncClient,
        container,
        fake_file,
    ):
        date_rent_start = datetime.now(UTC) + timedelta(4)
        payload = await self.generate_payload(
            date_rent_start=date_rent_start,
            date_rent_end=date_rent_start + timedelta(1),
        )
        files = {"poster": ("fake_image.jpg", fake_file, "image/jpeg")}
        response = await client.post(
            self.get_list_url(), data=payload, files=files
        )

        assert response.status_code == 200
        film_service = container.resolve(BaseFilmService)
        film = await film_service.get_by_id(response.json()["data"]["id"])
        assert film.id == response.json()["data"]["id"]
        payload.pop("date_rent_start")
        payload.pop("date_rent_end")
        for attr, value in payload.items():
            if hasattr(film, attr):
                if isinstance(getattr(film, attr), Enum):
                    assert getattr(film, attr).value == value
                else:
                    assert getattr(film, attr) == value

    async def test_create_film_with_wrong_startdate(
        self,
        client: AsyncClient,
        container,
        prepare_database,
        fake_file,
    ):
        date_rent_start = datetime.now(UTC) - timedelta(1)
        payload = await self.generate_payload(
            date_rent_start=date_rent_start,
            date_rent_end=date_rent_start + timedelta(1),
        )
        files = {"poster": ("fake_image.jpg", fake_file, "image/jpeg")}
        response = await client.post(
            self.get_list_url(), data=payload, files=files
        )
        assert response.status_code == 400
        film_service = container.resolve(BaseFilmService)
        films = await film_service.get_all()
        assert not films

    async def test_create_film_with_wrong_enddate(
        self,
        client: AsyncClient,
        container,
        prepare_database,
        fake_file,
    ):
        date_rent_start = datetime.now(UTC) - timedelta(1)
        payload = await self.generate_payload(
            date_rent_start=date_rent_start,
            date_rent_end=date_rent_start - timedelta(1),
        )
        files = {"poster": ("fake_image.jpg", fake_file, "image/jpeg")}
        response = await client.post(
            self.get_list_url(), data=payload, files=files
        )
        assert response.status_code == 400
        film_service = container.resolve(BaseFilmService)
        films = await film_service.get_all()
        assert not films

    async def test_get_film_sessions_by_id_film(
        self, client: AsyncClient, faker, prepare_database
    ):
        film = await FilmFactory().create()
        amount_film_sessions = faker.pyint(min_value=1, max_value=6)
        await FilmSessionFactory(film_id=film.id).create_batch(
            amount_film_sessions
        )
        response = await client.get(self.get_list_url(film.id, "sessions"))
        response_json = response.json()["data"]
        assert response.status_code == 200
        assert amount_film_sessions == len(response_json["film_sessions"])
        assert response_json["film_sessions"] == sorted(
            response_json["film_sessions"], key=lambda d: d["date_time"]
        )

    async def test_get_film_sessions_by_id_not_exist_film(
        self, client: AsyncClient, faker, prepare_database
    ):
        response = await client.get(
            self.get_list_url(faker.pyint(), "sessions")
        )
        response_json = response.json()
        assert response.status_code == 404
        assert response_json["message"] == FilmNotFoundException().message

    async def test_get_all_genres(
        self, client: AsyncClient, faker, prepare_database
    ):
        amount_genres = faker.pyint(max_value=20)
        await GenreFactory().create_batch(amount_genres)
        response = await client.get(self.get_list_url("genres"))
        response_json = response.json()["data"]
        assert response.status_code == 200
        assert len(response_json["genres"]) == amount_genres

    async def test_get_film_by_id(
        self, client: AsyncClient, faker, prepare_database
    ):
        for _i in range(faker.pyint(max_value=20)):
            film = await FilmFactory().create()
            response = await client.get(self.get_list_url(film.id))
            assert response.status_code == 200

    async def test_get_film_by_id_not_exist_id(
        self, client: AsyncClient, faker, prepare_database
    ):
        film = await FilmFactory().create()
        film.id = 10001
        response = await client.get(self.get_list_url(film.id))
        response_json = response.json()

        assert response.status_code == 404
        assert response_json["message"] == FilmNotFoundException().message

    async def test_delete_film_by_id_client(
        self, prepare_database, client: AsyncClient, faker
    ):
        film = await FilmFactory().create()

        response_delete = await client.delete(self.get_list_url(film.id))

        assert response_delete.status_code == 403
        assert response_delete.json()["detail"] == "Доступ запрещен"

    async def test_delete_film_by_id_employee(
        self, prepare_database, employee_client: AsyncClient, faker
    ):
        film = await FilmFactory().create()

        response_delete = await employee_client.delete(
            self.get_list_url(film.id)
        )
        response_search_after_delete = await employee_client.get(
            self.get_list_url(film.id)
        )

        assert response_delete.status_code == 200
        assert response_search_after_delete.status_code == 404

        assert (
            response_search_after_delete.json()["message"] == "Фильм не найден"
        )
        assert response_delete.json()["data"]["id"] == film.id
        assert response_delete.json()["data"]["status"] == "Фильм удален"

    async def test_delete_film_by_id_with_session_employee(
        self, prepare_database, employee_client: AsyncClient, faker
    ):
        film = await FilmFactory().create()
        await FilmSessionFactory(film_id=film.id).create()

        response_delete = await employee_client.delete(
            self.get_list_url(film.id)
        )

        assert response_delete.status_code == 400
        assert (
            response_delete.json()["message"]
            == "Невозможно удалить фильм с назначенным сеансом"
        )
