from dataclasses import dataclass
from typing import Any

from apps.cinema.models.halls import Hall
from apps.cinema.services.halls import (
    BaseHallService,
    BaseHallValidatorService,
)


@dataclass
class CreateHallUseCase:
    hall_service: BaseHallService
    validator_service: BaseHallValidatorService

    async def execute(self, hall_data: dict[str, Any]) -> Hall:
        await self.validator_service.validate(attributes=hall_data)
        return await self.hall_service.create(attributes=hall_data)
