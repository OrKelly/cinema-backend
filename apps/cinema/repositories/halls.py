from abc import abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from apps.cinema.models.halls import Hall
from core.database import Propagation, Transactional
from core.repositories.base import BaseORMRepository


@dataclass
class BaseHallRepository:
    @abstractmethod
    async def create(
        self, attributes: dict[str, Any] = None
    ) -> Hall | None: ...

    @abstractmethod
    async def get_by_title(self, title: str) -> Iterable[Hall] | None: ...

    @abstractmethod
    async def get_by_id(self, id_: int) -> Hall | None: ...

    @abstractmethod
    async def get_by_filter(
        self,
        field: str,
        value: Any,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ) -> Iterable[Hall] | list[None]: ...


@dataclass
class ORMHallRepository(BaseHallRepository, BaseORMRepository[Hall]):
    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, attributes: dict[str, Any] = None) -> Hall | None:
        return await super(BaseHallRepository, self).create(
            attributes=attributes
        )

    async def get_by_title(self, title: str) -> Iterable[Hall] | None:
        return await self.get_by(field="title", value=title)

    async def get_by_id(self, id_: int) -> Hall | None:
        return await self.get_by(field="id", value=id_)

    async def get_by_filter(
        self,
        field: str,
        value: Any,
        join_: set[str] = None,
        order_: dict | None = None,
    ) -> Iterable[Hall] | list[None]:
        return await self.get_by(field=field, value=value, join_=join_)
