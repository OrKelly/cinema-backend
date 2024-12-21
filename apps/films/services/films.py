from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, List

from apps.films.repositories.films import BaseFilmRepository
from apps.films.models.films import Film
from core.enums.films import AgeRatingEnum, FilmStatusEnum
from core.services.base import BaseOrmService


@dataclass
class BaseFilmService:
    repository: BaseFilmRepository

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
    ) -> Film | None: ...

    @abstractmethod
    async def get_by_rating(
        self,
        rating: AgeRatingEnum,
        join_: set[str, Any] = None,
        unique: bool = True,
        skip=0,
        limit=100,
    ) -> List[Film]: ...

    @abstractmethod
    async def get_by_status(
        self,
        status: FilmStatusEnum,
        join_: set[str, Any] = None,
        unique: bool = True,
        skip=0,
        limit=100,
    ) -> List[Film]: ...


@dataclass
class ORMFilmService(BaseFilmService, BaseOrmService):
    async def create(self, attributes: dict[str, Any]):
        return await super(BaseFilmService, self).create(attributes)

    async def get_all(
            self,
            skip=0,
            limit=100,
            join_=None,
            order_=None,
    ) -> List[Film]:
        return await super(BaseFilmService, self).get_all(
            skip=skip,
            limit=limit,
            join_=join_,
            order_=order_,
        )

    async def get_by_id(
            self, id_, join_: set[str] | None = None
    ) -> Film | None:
        return await super(BaseFilmService, self).get_by_id(
            id_=id_, join_=join_
        )

    async def get_by_rating(
            self,
            age_rating,
            join_=None,
            skip: int = 0,
            limit: int = 100,
    ):
        return await super(BaseFilmService, self).get_by_filter(
            filter_params={"age_rating": age_rating},
            join_=join_,
            skip=skip,
            limit=limit,
        )

    async def get_by_status(
            self,
            status,
            join_=None,
            skip=0,
            limit=100,
    ):
        return await super(BaseFilmService, self).get_by_filter(
            filter_params={"status": status},
            join_=join_,
            skip=skip,
            limit=limit,
        )
