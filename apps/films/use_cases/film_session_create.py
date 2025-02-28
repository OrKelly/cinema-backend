from dataclasses import dataclass
from typing import Any

from apps.films.services.film_sessions import (
    BaseFilmSessionService,
    BaseFilmSessionValidatorService,
)


@dataclass
class CreateFilmSessionUseCase:
    session_service: BaseFilmSessionService
    validator: BaseFilmSessionValidatorService

    async def execute(self, attributes: dict[Any, str]):
        await self.validator.validate(attributes)
        return await self.session_service.create(attributes)
