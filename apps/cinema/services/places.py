from abc import abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from apps.cinema.exceptions.places import (
    PlaceAlreadyExistsException,
    PlaceNotFoundException,
)
from apps.cinema.models.places import Place
from apps.cinema.repositories.places import BasePlaceRepository
from apps.cinema.repositories.rows import BaseRowRepository
from core.services.base import BaseOrmService


@dataclass
class BasePlaceService:
    repository: BasePlaceRepository
    row_repository: BaseRowRepository

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
    ) -> Place | None: ...

    @abstractmethod
    async def get_by_hall(
        self, hall_id: int
    ) -> Iterable[Place] | list[None]: ...

    @abstractmethod
    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] = None,
        order_: dict | None = None,
        unique: bool | None = False,
    ): ...


@dataclass
class ORMPlaceService(BasePlaceService, BaseOrmService):
    async def create(self, attributes: dict[str, Any]):
        return await super(BasePlaceService, self).create(attributes)

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ):
        return await super(BasePlaceService, self).get_all()

    async def get_by_id(
        self, id_: int, join_: set[str] | None = None
    ) -> Place | None:
        place = await super(BasePlaceService, self).get_by_id(
            id_=id_, join_=join_
        )
        if not place:
            raise PlaceNotFoundException()
        return place

    async def get_by_hall(self, hall_id: int) -> Iterable[Place] | list[None]:
        return await self.repository.get_by_hall(hall_id)

    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] = None,
        order_: dict | None = None,
        unique: bool | None = False,
    ):
        return await super(BasePlaceService, self).get_by_filter(
            filter_params=filter_params, join_=join_, order_=order_
        )


@dataclass
class BasePlaceValidatorService:
    @abstractmethod
    async def validate(self, attributes: dict[str, Any]) -> None: ...


@dataclass
class PlaceAlreadyExistsValidator(BasePlaceValidatorService):
    place_service: BasePlaceService

    async def validate(self, attributes: dict[str, Any]) -> None:
        place = await self.place_service.get_by_filter(
            filter_params={
                "place_id": attributes["place_id"],
                "number": attributes["number"],
            }
        )
        if place:
            raise PlaceAlreadyExistsException()
