from abc import abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from apps.films.exceptions.genres import GenreNotFoundException
from apps.films.models.genres import Genre
from apps.films.repositories.genres import BaseGenreRepository
from core.services.base import BaseOrmService


@dataclass
class BaseGenreService:
    repository: BaseGenreRepository

    @abstractmethod
    async def create(self, attributes: dict[str, Any]): ...

    @abstractmethod
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ) -> Iterable[Genre] | None: ...

    @abstractmethod
    async def get_by_id(
        self, id_: int, join_: set[str] | None = None
    ) -> Genre | None: ...


@dataclass
class ORMGenreService(BaseGenreService, BaseOrmService):
    async def create(self, attributes: dict[str, Any]):
        return await super(BaseGenreService, self).create(attributes)

    async def get_all(
        self,
        skip=0,
        limit=100,
        join_=None,
        order_=None,
    ) -> Iterable[Genre]:
        return await super(BaseGenreService, self).get_all(
            skip=skip,
            limit=limit,
            join_=join_,
            order_=order_,
        )

    async def get_by_id(
        self, id_, join_: set[str] | None = None
    ) -> Genre | None:
        genre = await super(BaseGenreService, self).get_by_id(
            id_=id_, join_=join_
        )
        if not genre:
            raise GenreNotFoundException()
        return genre
