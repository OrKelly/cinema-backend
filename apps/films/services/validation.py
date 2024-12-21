from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime, UTC

from apps.films.services.films import BaseFilmService
from apps.films.exceptions.rent_date import (
    EndDateIncorrectException, StartDateIncorrectException
)


@dataclass
class BaseValidationFilmService(ABC):
    @abstractmethod
    def validate(self, film_data: dict[str, any]) -> None: ...


@dataclass
class FilmRentDatesValidatorService(BaseValidationFilmService):
    film_service: BaseFilmService

    def validate(self, film_data):
        if film_data['date_rent_start'] > datetime.now(UTC):
            raise StartDateIncorrectException
        if film_data['date_rent_end'] > film_data['date_rent_start']:
            raise EndDateIncorrectException
