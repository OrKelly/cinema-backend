import io
from datetime import UTC, datetime, timedelta
from enum import Enum

import pytest
from httpx import AsyncClient

from apps.films.services.films import BaseFilmService
from core.enums.films import AgeRatingEnum, FilmStatusEnum
from tests.factories.halls import HallFactory


class TestFilmAPI:
    @staticmethod
    def get_list_url(*args, **kwargs):
        return "/".join(("api/v1/films/", *map(str, args)))

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
