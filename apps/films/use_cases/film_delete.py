from dataclasses import dataclass

from apps.films.services.film_sessions import FilmSessionCheckValidator
from apps.films.services.films import BaseFilmService


@dataclass
class DeleteFilmUseCase:
    film_service: BaseFilmService
    check_film_session_validator: FilmSessionCheckValidator

    async def delete_by_id(self, id_: int) -> None:
        film = await self.film_service.get_by_id(id_)
        await self.check_film_session_validator.validate_session(id_)
        await self.film_service.delete(film)
