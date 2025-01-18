from abc import abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from apps.cinema.exceptions.rows import (
    RowAlreadyExistsException,
    RowNotFoundException,
)
from apps.cinema.models.places import Place
from apps.cinema.models.rows import Row
from apps.cinema.repositories.rows import BaseRowRepository
from apps.cinema.services.places import BasePlaceService
from core.services.base import BaseOrmService


@dataclass
class BaseRowService:
    repository: BaseRowRepository
    place_service: BasePlaceService

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
    ) -> Row | None: ...

    @abstractmethod
    async def get_by_id_with_places(
        self, id_: int, join_: set[str] | None = None
    ) -> tuple[Row, Iterable[Place]] | None: ...

    @abstractmethod
    async def get_by_hall(
        self, hall_id: int
    ) -> Iterable[Row] | list[None]: ...

    @abstractmethod
    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] = None,
        order_: dict | None = None,
        unique: bool | None = False,
    ): ...

    @abstractmethod
    async def get_with_places_by_id(self, id_: int) -> Row: ...


@dataclass
class ORMRowService(BaseRowService, BaseOrmService):
    async def create(self, attributes: dict[str, Any]):
        row = await super(BaseRowService, self).create(attributes)
        place_attributes = {"row_id": row.id}
        for i in range(1, row.capacity + 1):
            place_attributes["number"] = i
            await self.place_service.create(attributes=place_attributes)
        return row

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ):
        return await super(BaseRowService, self).get_all()

    async def get_by_id(
        self, id_: int, join_: set[str] | None = None
    ) -> Row | None:
        row = await super(BaseRowService, self).get_by_id(id_=id_, join_=join_)
        if not row:
            raise RowNotFoundException()
        return row

    async def get_with_places_by_id(self, id_: int) -> Row:
        row = await self.get_by_filter(
            filter_params={"id": id_}, join_={"places"}, unique=True
        )
        if not row:
            raise RowNotFoundException
        return row[0]

    async def get_by_hall(self, hall_id: int) -> Iterable[Row] | list[None]:
        return await self.repository.get_by_hall(hall_id)

    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] = None,
        order_: dict | None = None,
        unique: bool | None = False,
    ):
        return await super(BaseRowService, self).get_by_filter(
            filter_params=filter_params,
            join_=join_,
            order_=order_,
            unique=unique,
        )


@dataclass
class BaseRowValidatorService:
    @abstractmethod
    async def validate(self, attributes: dict[str, Any]) -> None: ...


@dataclass
class RowAlreadyExistsValidator(BaseRowValidatorService):
    row_service: BaseRowService

    async def validate(self, attributes: dict[str, Any]) -> None:
        row = await self.row_service.get_by_filter(
            filter_params={
                "hall_id": attributes["hall_id"],
                "number": attributes["number"],
            }
        )
        if row:
            raise RowAlreadyExistsException()
