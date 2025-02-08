import io
from datetime import UTC, datetime, timedelta
from enum import Enum

import pytest
from httpx import AsyncClient

from apps.films.exceptions.films import FilmNotFoundException
from apps.films.services.film_sessions import BaseFilmSessionService
from apps.films.services.films import BaseFilmService
from core.enums.films import AgeRatingEnum, FilmStatusEnum
from tests.factories.film_sessions import FilmSessionFactory
from tests.factories.films import FilmFactory
from tests.factories.halls import HallFactory


class TestFilmAPI:
    @staticmethod
    def get_list_url(*args, **kwargs):
        return "api/v1/films/" + "/".join(map(str, args))

    @staticmethod
    def generate_fake_file(faker):
        # Generate fake file content
        file_content = faker.binary(length=1024)  # 1KB of random bytes
        # Create a file-like object
        file_bytes = io.BytesIO(file_content)
        # Set the name attribute (if required)
        file_bytes.name = "fake_image.jpg"
        return file_bytes

    @pytest.mark.asyncio
    async def test_create_film(
        self,
        client: AsyncClient,
        faker,
        container,
        minio_client,
        minio_cleanup,
        fake_file,
    ):
        hall = await HallFactory().create()
        date_rent_start = datetime.now(UTC) + timedelta(4)
        payload = {
            "cinemahall_id": hall.id,
            "title": faker.word(),
            "description": faker.text(),
            "age_rating": faker.enum(AgeRatingEnum).value,
            "duration": faker.pyfloat(),
            "status": faker.enum(FilmStatusEnum).value,
            "date_rent_start": date_rent_start.isoformat(),
            "date_rent_end": (date_rent_start + timedelta(1)).isoformat(),
        }

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
        faker,
        container,
        prepare_database,
        fake_file,
    ):
        hall = await HallFactory().create()
        date_rent_start = datetime.now(UTC) - timedelta(1)
        payload = {
            "cinemahall_id": hall.id,
            "title": faker.word(),
            "description": faker.text(),
            "age_rating": faker.enum(AgeRatingEnum).value,
            "duration": faker.pyfloat(),
            "status": faker.enum(FilmStatusEnum).value,
            "date_rent_start": date_rent_start.isoformat(),
            "date_rent_end": (date_rent_start + timedelta(1)).isoformat(),
        }
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
        faker,
        container,
        prepare_database,
        fake_file,
    ):
        hall = await HallFactory().create()
        date_rent_start = datetime.now(UTC) - timedelta(1)
        payload = {
            "cinemahall_id": hall.id,
            "title": faker.word(),
            "description": faker.text(),
            "age_rating": faker.enum(AgeRatingEnum).value,
            "duration": faker.pyfloat(),
            "status": faker.enum(FilmStatusEnum).value,
            "date_rent_start": date_rent_start.isoformat(),
            "date_rent_end": (date_rent_start - timedelta(1)).isoformat(),
        }
        files = {"poster": ("fake_image.jpg", fake_file, "image/jpeg")}
        response = await client.post(
            self.get_list_url(), data=payload, files=files
        )
        assert response.status_code == 400
        film_service = container.resolve(BaseFilmService)
        films = await film_service.get_all()
        assert not films

    async def test_get_film_sessions_by_id_film(
        self, client: AsyncClient, container, faker, prepare_database
    ):
        film = await FilmFactory().create()
        film_sessions_services = container.resolve(BaseFilmSessionService)
        amount_film_sessions = faker.pyint(min_value=1, max_value=6)
        film_sessions = await FilmSessionFactory().create_batch(
            amount_film_sessions
        )
        for session in film_sessions:
            await film_sessions_services.update(
                session.id, {"film_id": film.id}
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
