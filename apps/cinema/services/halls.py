from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

from apps.cinema.repositories.halls import BaseHallRepository
from apps.cinema.models.halls import Hall
from core.services.base import BaseOrmService
from apps.cinema.exceptions.halls import HallNotFoundException


@dataclass
class BaseHallService:
    repository: BaseHallRepository

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
        self,
        id_: int,
        join_: set[str, Any] | None = None,
    ) -> Hall | None: ...

    @abstractmethod
    async def get_filter(
        self,
        field: str,
        value: Any,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ): ...


@dataclass
class ORMHallService(BaseHallService, BaseOrmService):
    async def create(self, attributes: dict[str, Any]):
        return await super(BaseHallService, self).create(attributes)

    async def get_all(
            self,
            skip: int = 0,
            limit: int = 100,
            join_: set[str] = None,
            order_: dict | None = None,
    ): ...

    async def get_filter(
            self,
            field: str,
            value: Any,
            join_: set[str] = None,
            order_: dict | None = None
    ):
        return await super(BaseHallService, self).get_filter(
            field=field, value=value, join_=join_, order_=order_
        )

    async def get_by_id(
            self, id_: int, join_: set[str] | None = None
    ) -> Hall | None:
        hall = await super(BaseHallService, self).get_by_id(
            id_=id_, join_=join_
        )
        if not hall:
            raise HallNotFoundException(hall_id=id_)
        return hall

    async def get_by_title(self, title: str):
        hall = await self.get_filter(field="title", value=title)