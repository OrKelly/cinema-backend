from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime, UTC
from typing import Iterable

from apps.films.services.films import BaseFilmService
from apps.films.exceptions.rent_date import (
    EndDateIncorrectException, StartDateIncorrectException
)


@dataclass
class BaseFilmValidatorService(ABC):
    @abstractmethod
    def validate(self, film_data: dict[str, any]) -> None: ...


@dataclass
class FilmRentDatesValidatorService(BaseFilmValidatorService):
    film_service: BaseFilmService

    def validate(self, film_data: dict[str, any]):
        if film_data['date_rent_start'] >= datetime.now(UTC):
            raise StartDateIncorrectException
        if film_data['date_rent_end'] > film_data['date_rent_start']:
            raise EndDateIncorrectException


@dataclass
class ComposedFilmValidatorService(BaseFilmValidatorService):
    validators: Iterable[BaseFilmValidatorService]

    async def validate(self, film_data: dict[str, any]) -> None:
        for validator in self.validators:
            await validator.validate(film_data)
