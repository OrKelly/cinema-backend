from dataclasses import dataclass

from apps.films.services.films import BaseFilmService
from apps.films.services.validation import (
    BaseFilmDeleteValidatorService,
)


@dataclass
class DeleteFilmUseCase:
    film_service: BaseFilmService
    check_film_session_validator: BaseFilmDeleteValidatorService

    async def execute(self, id_: int) -> None:
        film = await self.film_service.get_by_id(id_)
        await self.check_film_session_validator.validate(
            film_data=film.to_dict()
        )
        await self.film_service.delete(film)
