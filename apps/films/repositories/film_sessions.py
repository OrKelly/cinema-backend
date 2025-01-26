from abc import abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import Select
from sqlalchemy.orm import selectinload

from apps.cinema.models import Hall
from apps.films.models import Film, FilmSession
from apps.users.models.users import User
from core.database import Propagation, Transactional
from core.repositories.base import BaseORMRepository


@dataclass
class BaseFilmSessionRepository:
    @abstractmethod
    async def create(
        self, attributes: dict[str, Any] = None
    ) -> FilmSession | None: ...

    @abstractmethod
    async def filter_by(
        self,
        filter_params: dict,
        join_: set[str, Any] = None,
        order_: dict | None = None,
        unique: bool = False,
    ) -> Iterable[FilmSession] | list[None]: ...

    @abstractmethod
    async def get_sessions_by_hall_id_and_date(
        self, hall_id: int, date_time: datetime, join_: set = None
    ) -> Iterable[FilmSession] | Iterable[None]: ...


@dataclass
class ORMFilmSessionRepository(
    BaseFilmSessionRepository, BaseORMRepository[FilmSession]
):
    @Transactional(propagation=Propagation.REQUIRED)
    async def create(
        self, attributes: dict[str, Any] = None
    ) -> FilmSession | None:
        return await super(BaseFilmSessionRepository, self).create(
            attributes=attributes
        )

    async def filter_by(
        self,
        filter_params: dict,
        join_: set[str, Any] = None,
        order_: dict | None = None,
        unique: bool = False,
    ) -> Iterable[User] | list[None]:
        return await super(BaseFilmSessionRepository, self).get_by_filter(
            filter_params=filter_params,
            join_=join_,
            order_=order_,
            unique=unique,
        )

    async def get_sessions_by_hall_id_and_date(
        self, hall_id: int, date_time: datetime, join_: set = None
    ) -> Iterable[FilmSession] | Iterable[None]:
        if join_ is None:
            join_ = {"film_hall"}
        start_of_day = date_time.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end_of_day = start_of_day + timedelta(days=1)
        query = self._query(join_)
        query = query.filter(
            Hall.id == hall_id,
            FilmSession.date_time >= start_of_day,
            FilmSession.date_time <= end_of_day,
        )
        return await self._all(query)

    def _join_film(self, query: Select):
        return query.join(FilmSession.film).options(
            selectinload(FilmSession.film)
        )

    def _join_film_hall(self, query: Select):
        return (
            query.join(FilmSession.film)
            .join(Film.hall)
            .options(selectinload(FilmSession.film).selectinload(Film.hall))
        )
