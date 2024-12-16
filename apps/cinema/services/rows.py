from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

from apps.cinema.exceptions.rows import RowAlreadyExists, RowNotFoundException
from apps.cinema.models.rows import Row
from apps.cinema.repositories.halls import BaseHallRepository
from apps.cinema.repositories.rows import BaseRowRepository
from core.services.base import BaseOrmService


@dataclass
class BaseRowService:
    repository: BaseRowRepository
    hall_repository: BaseHallRepository

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
    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] = None,
        order_: dict | None = None,
        unique: bool | None = False,
    ): ...


@dataclass
class ORMRowService(BaseRowService, BaseOrmService):
    async def create(self, attributes: dict[str, Any]):
        return await super(BaseRowService, self).create(attributes)

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ): ...

    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] = None,
        order_: dict | None = None,
        unique: bool | None = False,
    ):
        return await super(BaseRowService, self).get_by_filter(
            filter_params=filter_params, join_=join_, order_=order_
        )

    async def get_by_id(
        self, id_: int, join_: set[str] | None = None
    ) -> Row | None:
        row = await super(BaseRowService, self).get_by_id(id_=id_, join_=join_)
        if not row:
            raise RowNotFoundException(row_id=id_)
        return row


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
            raise RowAlreadyExists(row_number=attributes["number"])
