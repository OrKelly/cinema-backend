from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

from apps.cinema.exceptions.halls import (
    HallAlreadyExists,
    HallNotFoundException,
)
from apps.cinema.models.halls import Hall
from apps.cinema.repositories.halls import BaseHallRepository
from core.services.base import BaseOrmService


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
    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str, Any] = None,
        order_: dict | None = None,
        unique: bool | None = False,
    ): ...

    @abstractmethod
    async def get_by_title(self, title: str) -> Hall | None: ...


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

    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] = None,
        order_: dict | None = None,
        unique: bool | None = False,
    ):
        return await super(BaseHallService, self).get_by_filter(
            filter_params=filter_params, join_=join_, order_=order_
        )

    async def get_by_id(
        self, id_: int, join_: set[str] | None = None
    ) -> Hall | None:
        hall = await super(BaseHallService, self).get_by_id(
            id_=id_, join_=join_
        )
        if not hall:
            raise HallNotFoundException()
        return hall

    async def get_by_title(self, title: str) -> Hall | None:
        return await self.get_by_filter(
            filter_params={"title": title}, unique=True
        )


@dataclass
class BaseHallValidatorService:
    @abstractmethod
    async def validate(self, attributes: dict[str, Any]) -> None: ...


@dataclass
class UniqueTitleHallValidatorService(BaseHallValidatorService):
    hall_service: BaseHallService

    async def validate(self, attributes: dict[str, Any]) -> None:
        hall = await self.hall_service.get_by_title(title=attributes["title"])
        if hall:
            raise HallAlreadyExists()
