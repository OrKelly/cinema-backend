from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from apps.orders.models.order import Order
from core.database import Propagation, Transactional
from core.repositories.base import BaseORMRepository


@dataclass
class BaseOrderRepository(ABC):
    @abstractmethod
    async def create(
        self, attributes: dict[str, Any] = None
    ) -> Order | None: ...

    @abstractmethod
    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] = None,
        order_: dict | None = None,
        skip: int = 0,
        limit: int = 100,
        unique: bool = False,
    ) -> Iterable[Order] | Iterable[None] | Order: ...


@dataclass
class ORMOrderRepository(BaseOrderRepository, BaseORMRepository[Order]):
    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, attributes: dict[str, Any] = None) -> Order | None:
        return await super(BaseOrderRepository, self).create(
            attributes=attributes
        )

    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] = None,
        order_: dict | None = None,
        skip: int = 0,
        limit: int = 100,
        unique: bool = False,
    ) -> Iterable[Order] | Iterable[None] | Order:
        return await super(BaseOrderRepository, self).get_by_filter(
            filter_params=filter_params,
            join_=join_,
            skip=skip,
            limit=limit,
            order_=order_,
            unique=unique,
        )
