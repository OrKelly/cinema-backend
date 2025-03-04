from abc import abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from apps.cinema.models import Row
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
    async def get_by_title(self, title: str) -> Hall | None: ...

    @abstractmethod
    async def get_by_id(self, id_: int) -> Hall | None: ...

    @abstractmethod
    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str, Any] = None,
        order_: dict | None = None,
        skip: int = 0,
        limit: int = 100,
        unique: bool = False,
    ) -> Iterable[Hall] | list[None]: ...


@dataclass
class ORMHallRepository(BaseHallRepository, BaseORMRepository[Hall]):
    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, attributes: dict[str, Any] = None) -> Hall | None:
        return await super(BaseHallRepository, self).create(
            attributes=attributes
        )

    async def get_by_title(self, title: str) -> Hall | None:
        return await super(BaseHallRepository, self).get_by(
            field="title", value=title
        )

    async def get_by_id(self, id_: int) -> Hall | None:
        return await super(BaseHallRepository, self).get_by(
            field="id", value=id_
        )

    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str, Any] = None,
        order_: dict | None = None,
        skip: int = 0,
        limit: int = 100,
        unique: bool = False,
    ) -> Iterable[Hall] | list[None]:
        return await super(BaseHallRepository, self).get_by_filter(
            filter_params=filter_params,
            join_=join_,
            order_=order_,
            skip=skip,
            limit=limit,
            unique=unique,
        )

    def _join_rows(self, query: Select):
        return query.options(joinedload(Hall.rows).joinedload(Row.places))
