from abc import abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from apps.films.models.films import Film
from core.database import Propagation, Transactional
from core.repositories.base import BaseORMRepository


@dataclass
class BaseFilmRepository:
    @abstractmethod
    async def create(
        self, attributes: dict[str, Any] = None
    ) -> Film | None: ...

    @abstractmethod
    async def get_by_id(self, id: int) -> Film | None: ...

    @abstractmethod
    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str, Any] = None,
        order_: dict | None = None,
        unique: bool = False,
    ) -> Iterable[Film] | list[None]: ...


@dataclass
class ORMFilmRepository(BaseFilmRepository, BaseORMRepository[Film]):
    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, attributes: dict[str, Any] = None) -> Film | None:
        return await super(BaseFilmRepository, self).create(
            attributes=attributes
        )

    async def get_by_id(self, id_: int) -> Film | None:
        return await self.get_by(field="id", value=id_)

    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str, Any] = None,
        order_: dict | None = None,
        unique: bool = False,
    ) -> Iterable[Film] | list[None]:
        return await super(BaseFilmRepository, self).get_by_filter(
            filter_params=filter_params,
            join_=join_,
            order_=order_,
            unique=unique,
        )
