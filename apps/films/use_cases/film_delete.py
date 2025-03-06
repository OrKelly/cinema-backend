from dataclasses import dataclass

from apps.films.exceptions.film_sessions import FilmSessionAssignedException
from apps.films.services.film_sessions import BaseFilmSessionService
from apps.films.services.films import BaseFilmService


@dataclass
class DeleteFilmUseCase:
    film_service: BaseFilmService
    film_session_service: BaseFilmSessionService

    async def delete_by_id(self, id_: int) -> None:
        film = await self.film_service.get_by_id(id_)

        film_sessions = (
            await self.film_session_service.get_sessions_by_film_id(id_)
        )

        if film_sessions:
            raise FilmSessionAssignedException()

        await self.film_service.delete(film)
