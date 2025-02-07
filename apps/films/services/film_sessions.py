import datetime
from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

import pytz

from apps.films.exceptions.film_sessions import (
    FilmSessionDateConflict,
    FilmSessionIncorrectDateException,
    FilmSessionNotFoundException,
)
from apps.films.exceptions.films import FilmNotFoundException
from apps.films.models import Film, FilmSession
from apps.films.repositories.film_sessions import BaseFilmSessionRepository
from apps.films.services.films import BaseFilmService
from core.services.base import BaseOrmService


@dataclass
class BaseFilmSessionService(ABC):
    repository: BaseFilmSessionRepository
    film_services: BaseFilmService

    @abstractmethod
    async def create(self, attributes: dict[str, Any]): ...

    @abstractmethod
    async def get_by_id(
        self, id_: int, join_: set[str] | None = None
    ) -> FilmSession | None: ...

    @abstractmethod
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ): ...

    @abstractmethod
    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] = None,
        order_: dict | None = None,
        unique: bool | None = False,
    ): ...

    @abstractmethod
    async def get_sessions_by_hall_id_and_date(
        self, hall_id: int, date_time: datetime, join_: set | None = None
    ) -> Iterable[FilmSession] | Iterable[None]: ...

    @abstractmethod
    async def get_sessions_by_film_id(
        self, film_id: int
    ) -> Iterable[FilmSession] | Iterable[None]: ...


@dataclass
class ORMFilmSessionService(BaseFilmSessionService, BaseOrmService):
    async def create(self, attributes: dict[str, Any]):
        return await self.repository.create(attributes)

    async def get_by_id(
        self, id_: int, join_: set[str] | None = None
    ) -> FilmSession | None:
        session = await super(BaseFilmSessionService, self).get_by_id(
            id_=id_, join_=join_
        )
        if not session:
            raise FilmSessionNotFoundException()
        return session

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ):
        return await super(BaseFilmSessionService, self).get_all(
            skip=skip,
            limit=limit,
            join_=join_,
            order_=order_,
        )

    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] = None,
        order_: dict | None = None,
        unique: bool | None = False,
    ):
        return await super(BaseFilmSessionService, self).get_by_filter(
            filter_params=filter_params, join_=join_, order_=order_
        )

    async def get_sessions_by_hall_id_and_date(
        self, hall_id: int, date_time: datetime, join_: set | None = None
    ) -> Iterable[FilmSession] | Iterable[None]:
        return await self.repository.get_sessions_by_hall_id_and_date(
            hall_id, date_time, join_
        )

    async def get_sessions_by_film_id(
        self, film_id: int
    ) -> Iterable[FilmSession] | Iterable[None]:
        await FilmSessionValidatorService(self.film_services).validate(
            attributes={"film_id": film_id}
        )
        return await self.get_by_filter(
            filter_params={"film_id": film_id}, order_={"asc": ["date_time"]}
        )


@dataclass
class BaseFilmSessionValidatorService(ABC):
    @abstractmethod
    async def validate(
        self, attributes: dict[str, Any], *args, **kwargs
    ) -> None: ...


@dataclass
class FilmSessionValidatorService(BaseFilmSessionValidatorService):
    film_service: BaseFilmService

    async def validate(
        self, attributes: dict[str, Any], *args, **kwargs
    ) -> None:
        film = await self.get_film(attributes)
        if not film:
            raise FilmNotFoundException
        timezone = pytz.UTC
        date_time = attributes.get("date_time")
        if date_time:
            if date_time.tzinfo is None:
                date_time = timezone.localize(date_time)
            if (
                film.date_rent_start > date_time
                or film.date_rent_end < date_time
            ):
                raise FilmSessionIncorrectDateException

    async def get_film(self, attributes: dict[str, Any]) -> Film:
        return await self.film_service.get_by_id(attributes["film_id"])


@dataclass
class FilmSessionIsDateTimeFreeValidatorService(
    BaseFilmSessionValidatorService
):
    session_service: BaseFilmSessionService
    film_service: BaseFilmService

    async def validate(
        self, attributes: dict[str, Any], *args, **kwargs
    ) -> None:
        film = await self.get_film(attributes["film_id"])
        sessions = await self.get_film_sessions(film, attributes["date_time"])
        for session in sessions:
            if not self.validate_session(
                session=session,
                film=film,
                session_date=attributes["date_time"],
            ):
                raise FilmSessionDateConflict

    async def get_film(self, film_id: int) -> Film:
        return await self.film_service.get_by_id(id_=film_id)

    async def get_film_sessions(
        self, film: Film, date_time: datetime
    ) -> Iterable[FilmSession] | None:
        return await self.session_service.get_sessions_by_hall_id_and_date(
            hall_id=film.cinemahall_id, date_time=date_time
        )

    def validate_session(
        self, session: FilmSession, film: Film, session_date: datetime.datetime
    ) -> bool:
        session_end_time = session.date_time + datetime.timedelta(
            minutes=session.film.duration
        )
        new_session_end_time = session_date + datetime.timedelta(
            minutes=film.duration
        )

        if session.date_time < session_date:
            return session_end_time <= session_date

        return new_session_end_time <= session.date_time


@dataclass
class ComposedFilmSessionValidator(BaseFilmSessionValidatorService):
    validators: Iterable[BaseFilmSessionValidatorService]

    async def validate(
        self, attributes: dict[str, Any], *args, **kwargs
    ) -> None:
        for validator in self.validators:
            await validator.validate(attributes, args, kwargs)
