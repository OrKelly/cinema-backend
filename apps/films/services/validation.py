from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime

from apps.films.exceptions.film_sessions import FilmSessionAssignedException
from apps.films.exceptions.rent_date import (
    EndDateIncorrectException,
    StartDateIncorrectException,
)
from apps.films.services.film_sessions import BaseFilmSessionService
from apps.films.services.films import BaseFilmService
from apps.films.services.genres import BaseGenreService
from apps.films.exceptions.genres import GenreExistValidateException


@dataclass
class BaseFilmValidatorService(ABC):
    @abstractmethod
    async def validate(self, film_data: dict[str, any]) -> None: ...


@dataclass
class FilmRentDatesValidatorService(BaseFilmValidatorService):
    film_service: BaseFilmService

    async def validate(self, film_data: dict[str, any]):
        if film_data["date_rent_start"] < datetime.now(UTC):
            raise StartDateIncorrectException
        if film_data["date_rent_end"] <= film_data["date_rent_start"]:
            raise EndDateIncorrectException


@dataclass
class ComposedFilmValidatorService(BaseFilmValidatorService):
    validators: Iterable[BaseFilmValidatorService]

    async def validate(self, film_data: dict[str, any]) -> None:
        for validator in self.validators:
            await validator.validate(film_data)


@dataclass
class BaseFilmDeleteValidatorService(ABC):
    @abstractmethod
    def validate(self, film_data: dict[str, any]) -> None: ...


@dataclass
class FilmSessionCheckValidator(BaseFilmDeleteValidatorService):
    film_session_service: BaseFilmSessionService

    async def validate(self, film_data: dict[str, any]) -> None:
        film_sessions = (
            await self.film_session_service.get_sessions_by_film_id(
                film_data["id"]
            )
        )

        if film_sessions:
            raise FilmSessionAssignedException()


@dataclass
class FilmGenresValidatorService(BaseFilmValidatorService):
    genre_service: BaseGenreService

    async def validate(self, film_data: dict[str, any]):
        genres = await self.genre_service.get_all()
        exists_genres_ids = {genre.id for genre in genres}
        selected_genres_ids = set(film_data.get('genres', {}))
        error_ids = selected_genres_ids.difference(exists_genres_ids)
        if error_ids:
            raise GenreExistValidateException(error_ids)
