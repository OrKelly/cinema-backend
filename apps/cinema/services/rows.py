from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

from apps.cinema.exceptions.halls import HallNotFoundException
from apps.cinema.exceptions.rows import RowNotFoundException
from apps.cinema.models.rows import Row
from apps.cinema.repositories.halls import BaseHallRepository
from apps.cinema.repositories.rows import BaseRowRepository
from core.services.base import BaseOrmService


@dataclass
class BaseRowService:
    repository: BaseRowRepository
    hall_repository: BaseHallRepository

    @abstractmethod
    async def create(self, attributes: dict[str, Any]): ...

    @abstractmethod
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ): ...

    @abstractmethod
    async def get_by_id(
        self, id_: int, join_: set[str] | None = None
    ) -> Row | None: ...

    @abstractmethod
    async def get_by_filter(
        self,
        field: str,
        value: Any,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ): ...


@dataclass
class ORMRowService(BaseRowService, BaseOrmService):
    async def create(self, attributes: dict[str, Any]):
        exists_hall = await self.hall_repository.get_by_id(
            id_=attributes["hall_id"]
        )
        if not exists_hall:
            raise HallNotFoundException
        return await super(BaseRowService, self).create(attributes)

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ): ...

    async def get_by_filter(
        self,
        field: str,
        value: Any,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ):
        return await super(BaseRowService, self).get_filter(
            field=field, value=value, join_=join_, order_=order_
        )

    async def get_by_id(
        self, id_: int, join_: set[str] | None = None
    ) -> Row | None:
        row = await super(BaseRowService, self).get_by_id(id_=id_, join_=join_)
        if not row:
            raise RowNotFoundException(row_id=id_)
        return row
