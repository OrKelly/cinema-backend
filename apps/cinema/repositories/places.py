from abc import abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from apps.cinema.models.places import Place
from core.database import Propagation, Transactional
from core.repositories.base import BaseORMRepository


@dataclass
class BasePlaceRepository:
    @abstractmethod
    async def create(
        self, attributes: dict[str, Any] = None
    ) -> Place | None: ...

    @abstractmethod
    async def get_by_id(self, id_: int) -> Place | None: ...

    @abstractmethod
    async def get_by_hall(self, hall_id: int) -> list[Place] | None: ...

    @abstractmethod
    async def get_by_filter(
        self,
        field: str,
        value: Any,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ) -> Iterable[Place] | list[None]: ...


@dataclass
class ORMPlaceRepository(BasePlaceRepository, BaseORMRepository[Place]):
    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, attributes: dict[str, Any] = None) -> Place | None:
        return await super(BasePlaceRepository, self).create(
            attributes=attributes,
        )

    async def get_by_id(self, id_: int) -> Place | None:
        return await self.get_by(field="id", value=id_)

    async def get_by_hall(self, hall_id: int) -> Iterable[Place] | list[None]:
        return await self.get_by(field="hall", value=hall_id)

    async def get_by_filter(
        self,
        field: str,
        value: Any,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ) -> Iterable[Place] | list[None]:
        return await self.get_by(field=field, value=value, join_=join_)
