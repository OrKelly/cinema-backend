from abc import abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any


from apps.cinema.models.rows import Row
from core.database import Propagation, Transactional
from core.repositories.base import BaseORMRepository


@dataclass
class BaseRowRepository:
    @abstractmethod
    async def create(self, attributes: dict[str, Any] = None) -> Row | None: ...

    @abstractmethod
    async def get_by_id(self, id_: int) -> Row | None: ...

    @abstractmethod
    async def get_by_hall(self, hall_id: int) -> list[Row] | None: ...

    @abstractmethod
    async def get_by_filter(
            self,
            field: str,
            value: Any,
            join_: set[str, Any] = None,
            order_: dict | None = None,
    ) -> Iterable[Row] | list[None]: ...


@dataclass
class ORMRowRepository(BaseRowRepository, BaseORMRepository[Row]):
    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, attributes: dict[str, Any] = None) -> Row | None:
        return await super(BaseRowRepository, self).create(
            attributes=attributes,
        )

    async def get_by_id(self, id_: int) -> Row | None:
        return await self.get_by(field='id', value=id_)

    async def get_by_hall(self, hall_id: int) -> Iterable[Row] | list[None]:
        return await self.get_by(field='hall', value=hall_id)

    async def get_by_filter(
        self,
        field: str,
        value: Any,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ) -> Iterable[Row] | list[None]:
        return await self.get_by(field=field, value=value, join_=join_)


