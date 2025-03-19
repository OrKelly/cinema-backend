from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from apps.orders.models.ticket import Ticket
from core.database import Propagation, Transactional
from core.repositories.base import BaseORMRepository


@dataclass
class BaseTicketRepository(ABC):
    @abstractmethod
    async def create(
        self, attributes: dict[str, Any] = None
    ) -> Ticket | None: ...

    @abstractmethod
    async def get_by_id(self, id_: int) -> Ticket | None: ...

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


@dataclass
class ORMTicketRepository(BaseTicketRepository, BaseORMRepository[Ticket]):
    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, attributes: dict[str, Any] = None) -> Ticket | None:
        return await super(BaseTicketRepository, self).create(
            attributes=attributes
        )

    async def get_by_id(self, id_: int) -> Ticket | None:
        return await super(BaseTicketRepository, self).get_by(
            field="id", value=id_, unique=True
        )

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ) -> Iterable[Ticket] | Ticket | None:
        return await super(BaseTicketRepository, self).get_all(
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
        return await super(BaseTicketRepository, self).get_by_filter(
            filter_params=filter_params,
            join_=join_,
            skip=skip,
            limit=limit,
            order_=order_,
            unique=unique,
        )
