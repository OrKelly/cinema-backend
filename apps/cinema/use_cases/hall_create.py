from dataclasses import dataclass
from typing import Any

from apps.cinema.models.halls import Hall
from apps.cinema.services.halls import BaseHallService


@dataclass
class CreateHallUseCase:
    hall_service: BaseHallService
    # можно сюда добавить дополнительную
    # проверку уникальности наименования

    async def execute(
            self, hall_data: dict[str, Any]
    ) -> Hall:
        return await self.hall_service.create(attributes=hall_data)
