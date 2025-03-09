from dataclasses import dataclass

from apps.films.exceptions.film_sessions import FilmSessionAssignedException
from apps.films.services.film_sessions import BaseFilmSessionService


@dataclass
class FilmSessionCheckUseCase:
    film_session_service: BaseFilmSessionService

    async def check_film_session(self, id_: int) -> bool:
        film_sessions = (
            await self.film_session_service.get_sessions_by_film_id(id_)
        )

        if film_sessions:
            raise FilmSessionAssignedException()

        return False
