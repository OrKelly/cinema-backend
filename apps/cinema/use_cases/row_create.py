from dataclasses import dataclass
from typing import Any

from apps.cinema.models.rows import Row
from apps.cinema.services.halls import BaseHallService
from apps.cinema.services.rows import BaseRowService, BaseRowValidatorService


@dataclass
class CreateRowUseCase:
    row_service: BaseRowService
    hall_service: BaseHallService
    validator_service: BaseRowValidatorService

    async def execute(self, attributes: dict[str, Any]) -> Row:
        await self.hall_service.get_by_id(id_=attributes["hall_id"])
        await self.validator_service.validate(attributes=attributes)
        return await self.row_service.create(attributes)
