from abc import abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from apps.films.models.genres import Genre
from core.database import Propagation, Transactional
from core.repositories.base import BaseORMRepository


@dataclass
class BaseGenreRepository:
    @abstractmethod
    async def create(
        self, attributes: dict[str, Any] = None
    ) -> Genre | None: ...

    @abstractmethod
    async def get_by_id(self, id: int) -> Genre | None: ...

    @abstractmethod
    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str, Any] = None,
        order_: dict | None = None,
        unique: bool = False,
    ) -> Iterable[Genre] | list[None]: ...


@dataclass
class ORMGenreRepository(BaseGenreRepository, BaseORMRepository[Genre]):
    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, attributes: dict[str, Any] = None) -> Genre | None:
        return await super(BaseGenreRepository, self).create(
            attributes=attributes
        )

    async def get_by_id(self, id_: int) -> Genre | None:
        return await self.get_by(field="id", value=id_)

    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str, Any] = None,
        order_: dict | None = None,
        unique: bool = False,
    ) -> Iterable[Genre] | list[None]:
        return await super(BaseGenreRepository, self).get_by_filter(
            filter_params=filter_params,
            join_=join_,
            order_=order_,
            unique=unique,
        )
