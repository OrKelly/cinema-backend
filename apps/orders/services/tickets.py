from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from apps.orders.exceptions.tickets import (
    TicketForOrderAlreadyExistException,
    TicketNotFoundException,
)
from apps.orders.models.ticket import Ticket
from apps.orders.repositories.tickets import BaseTicketRepository
from core.services.base import BaseOrmService


@dataclass
class BaseTicketService(ABC):
    repository: BaseTicketRepository

    @abstractmethod
    async def create(self, attributes: dict[str, Any]): ...

    @abstractmethod
    async def get_by_id(
        self, id_: int, join_: set[str] | None = None
    ) -> Ticket | None: ...

    @abstractmethod
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ) -> Iterable[Ticket] | Ticket | None: ...

    @abstractmethod
    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] = None,
        order_: dict | None = None,
        skip: int = 0,
        limit: int = 100,
        unique: bool = False,
    ) -> Iterable[Ticket] | Iterable[None] | Ticket: ...

    @abstractmethod
    async def update(
        self, id_: int, attributes: dict[str, Any]
    ) -> Ticket | None: ...


@dataclass
class ORMTicketService(BaseTicketService, BaseOrmService):
    async def create(self, attributes: dict[str, Any]):
        return await super(BaseTicketService, self).create(
            attributes=attributes
        )

    async def get_by_id(
        self, id_: int, join_: set[str] | None = None
    ) -> Ticket | None:
        ticket = await super(BaseTicketService, self).get_by_id(
            id_=id_, join_=join_
        )
        if not ticket:
            raise TicketNotFoundException()
        return ticket

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ) -> Iterable[Ticket] | Ticket | None:
        return await super(BaseTicketService, self).get_all(
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
        skip: int = 0,
        limit: int = 100,
        unique: bool = False,
    ) -> Iterable[Ticket] | Iterable[None] | Ticket:
        return await super(BaseTicketService, self).get_by_filter(
            filter_params=filter_params,
            join_=join_,
            order_=order_,
            skip=skip,
            limit=limit,
            unique=unique,
        )

    async def update(
        self, id_: int, attributes: dict[str, Any]
    ) -> Ticket | None:
        return await super(BaseTicketService, self).update(
            id_=id_,
            attributes=attributes,
        )


@dataclass
class BaseTicketValidatorService(ABC):
    @abstractmethod
    async def validate(self, attributes: dict[str, Any]) -> None: ...


@dataclass
class ExistsTicketForOrderValidatorService(BaseTicketValidatorService):
    ticket_repository: BaseTicketRepository

    async def validate(self, attributes: dict[str, Any]) -> None:
        if order_id := attributes.get("order_id"):
            ticket = await self.ticket_repository.get_by_filter(
                filter_params={"order_id": order_id}
            )
            if ticket:
                raise TicketForOrderAlreadyExistException
