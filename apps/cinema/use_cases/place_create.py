from dataclasses import dataclass
from typing import Any

from apps.cinema.models.places import Place
from apps.cinema.services.places import (
    BasePlaceService,
    BasePlaceValidatorService,
)
from apps.cinema.services.rows import BaseRowService


@dataclass
class CreatePlaceUseCase:
    row_service: BaseRowService
    place_service: BasePlaceService
    validator_service: BasePlaceValidatorService

    async def execute(self, attributes: dict[str, Any]) -> Place:
        await self.row_service.get_by_id(id_=attributes["row_id"])
        await self.validator_service.validate(attributes=attributes)
        return await self.place_service.create(attributes)
