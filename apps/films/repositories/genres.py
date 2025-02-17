from abc import abstractmethod
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


@dataclass
class ORMGenreRepository(BaseGenreRepository, BaseORMRepository[Genre]):
    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, attributes: dict[str, Any] = None) -> Genre | None:
        return await super(BaseGenreRepository, self).create(
            attributes=attributes
        )

    async def get_by_id(self, id_: int) -> Genre | None:
        return await self.get_by(field="id", value=id_)
