from dataclasses import dataclass
from typing import Any


from apps.films.services.films import BaseFilmService
from apps.films.services.validation import BaseValidationFilmService


@dataclass
class BaseValidationFilmUseCase:
    film_sevice: BaseFilmService
    validator: BaseValidationFilmService

    async def execute(self, film_data: dict[str, Any]): ...


@dataclass
class ValidationFilmUseCase(BaseValidationFilmUseCase):
    async def execute(self, film_data):
        return await self.validator.validate(film_data)
