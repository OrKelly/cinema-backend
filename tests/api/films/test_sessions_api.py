import datetime

from httpx import AsyncClient

from apps.films.services.film_sessions import BaseFilmSessionService
from core.database import get_session
from tests.factories.film_sessions import FilmSessionFactory
from tests.factories.films import FilmFactory
from tests.factories.halls import HallFactory


class TestFilmAPI:
    @staticmethod
    def get_list_url(**kwargs):
        return "api/v1/films/sessions"

    async def test_create_film_session(
        self,
        client: AsyncClient,
        faker,
        container,
        current_date_time,
        prepare_database,
    ):
        date_time = datetime.date.today()
        film = await FilmFactory(
            date_rent_start=date_time,
            date_rent_end=date_time + datetime.timedelta(days=7),
        ).create()
        hall = await HallFactory().create()
        payload = {
            "film_id": film.id,
            "hall_id": hall.id,
            "date_time": current_date_time.strftime("%Y-%m-%d"),
            "price": faker.pyint(min_value=100, max_value=1000),
        }
        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 200

        film_session_service: BaseFilmSessionService = container.resolve(
            BaseFilmSessionService
        )
        session = await film_session_service.get_by_id(
            id_=response.json()["data"]["id"]
        )
        assert session.id == response.json()["data"]["id"]
        payload.pop("date_time")
        assert all(
            [
                str(getattr(session, attr)) == str(value)
                for attr, value in payload.items()
                if hasattr(session, attr)
            ]
        )

    async def test_create_film_session_with_incorrect_date_time(
        self, client, faker, container, current_date_time, prepare_database
    ):
        film = await FilmFactory(
            date_rent_start=current_date_time + datetime.timedelta(days=7),
            date_rent_end=current_date_time + datetime.timedelta(days=14),
        ).create()
        hall = await HallFactory().create()
        payload = {
            "film_id": film.id,
            "hall_id": hall.id,
            "date_time": current_date_time.strftime("%Y-%m-%d"),
            "price": faker.pyfloat(
                max_value=10000, min_value=100, right_digits=2
            ),
        }
        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 400

        film_session_service: BaseFilmSessionService = container.resolve(
            BaseFilmSessionService
        )
        sessions = await film_session_service.get_all()
        assert not sessions

        async with get_session() as session:
            film.date_rent_start = current_date_time - datetime.timedelta(
                days=14
            )
            film.date_rent_end = current_date_time + datetime.timedelta(
                days=14
            )
            await session.commit()

        payload = {
            "film_id": film.id,
            "hall_id": hall.id,
            "date_time": current_date_time.strftime("%Y-%m-%d"),
            "price": faker.pyfloat(
                max_value=10000, min_value=100, right_digits=2
            ),
        }
        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 400

        sessions = await film_session_service.get_all()
        assert not sessions

    async def test_create_film_session_with_conflict_sessions_at_same_film(
        self, client, faker, container, current_date_time, prepare_database
    ):
        film = await FilmFactory(
            date_rent_start=current_date_time - datetime.timedelta(days=1),
            duration=120,
            date_rent_end=current_date_time + datetime.timedelta(days=7),
        ).create()
        hall = await HallFactory().create()
        await FilmSessionFactory(
            date_time=current_date_time
            + datetime.timedelta(hours=2, minutes=30),
            film_id=film.id,
            hall_id=hall.id,
        ).create()
        await FilmSessionFactory(
            date_time=current_date_time - datetime.timedelta(hours=1),
            film_id=film.id,
            hall_id=hall.id,
        ).create()
        conflict_time = current_date_time + datetime.timedelta(hours=1)
        # Сессия будет налезать на первую сессию, начинающуюся позже
        payload = {
            "film_id": film.id,
            "hall_id": hall.id,
            "date_time": conflict_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
            + "Z",
            "price": faker.pyfloat(
                max_value=10000, min_value=100, right_digits=2
            ),
        }
        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 400
        film_session_service: BaseFilmSessionService = container.resolve(
            BaseFilmSessionService
        )
        sessions = await film_session_service.get_by_filter(
            filter_params={"film_id": film.id, "price": payload["price"]}
        )
        assert not sessions

        # Сессия будет налезать на вторую сессию, начинающуюся раньше
        payload["date_time"] = (
            current_date_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        )

        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 400
        sessions = await film_session_service.get_by_filter(
            filter_params={"film_id": film.id, "price": payload["price"]}
        )
        assert not sessions

    async def test_create_film_session_with_conflict_sessions_at_same_hall(
        self, client, faker, container, current_date_time, prepare_database
    ):
        hall = await HallFactory().create()
        film1 = await FilmFactory(
            date_rent_start=current_date_time - datetime.timedelta(days=1),
            duration=120,
            date_rent_end=current_date_time + datetime.timedelta(days=7),
        ).create()
        film2 = await FilmFactory(
            date_rent_start=current_date_time - datetime.timedelta(days=1),
            duration=120,
            date_rent_end=current_date_time + datetime.timedelta(days=7),
        ).create()
        await FilmSessionFactory(
            date_time=current_date_time
            + datetime.timedelta(hours=2, minutes=30),
            film_id=film1.id,
            hall_id=hall.id,
        ).create()
        await FilmSessionFactory(
            date_time=current_date_time - datetime.timedelta(hours=1),
            film_id=film2.id,
            hall_id=hall.id,
        ).create()
        new_film = await FilmFactory(
            date_rent_start=current_date_time - datetime.timedelta(days=1),
            duration=120,
            date_rent_end=current_date_time + datetime.timedelta(days=7),
        ).create()

        conflict_time = current_date_time + datetime.timedelta(hours=1)
        payload = {
            "film_id": new_film.id,
            "hall_id": hall.id,
            "date_time": conflict_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
            + "Z",
            "price": faker.pyfloat(
                max_value=10000, min_value=100, right_digits=2
            ),
        }
        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 400
        film_session_service: BaseFilmSessionService = container.resolve(
            BaseFilmSessionService
        )
        sessions = await film_session_service.get_by_filter(
            filter_params={"film_id": new_film.id, "price": payload["price"]}
        )
        assert not sessions

        payload["date_time"] = (
            current_date_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        )
        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 400
        sessions = await film_session_service.get_by_filter(
            filter_params={"film_id": new_film.id, "price": payload["price"]}
        )
        assert not sessions
