from dataclasses import dataclass

from apps.films.services.films import BaseFilmService
from apps.films.use_cases.film_session_check import FilmSessionCheckUseCase


@dataclass
class DeleteFilmUseCase:
    film_service: BaseFilmService
    check_film_session: FilmSessionCheckUseCase

    async def delete_by_id(self, id_: int) -> None:
        film = await self.film_service.get_by_id(id_)
        session = await self.check_film_session.check_film_session(id_=id_)

        if not session:
            await self.film_service.delete(film)
