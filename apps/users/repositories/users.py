from abc import abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from apps.users.models.users import User
from core.database import Propagation, Transactional
from core.repositories.base import BaseORMRepository


@dataclass
class BaseUserRepository:
    @abstractmethod
    async def create(
        self, attributes: dict[str, Any] = None
    ) -> User | None: ...

    @abstractmethod
    async def get_by_id(self, id_: int) -> User | None: ...

    @abstractmethod
    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] = None,
        order_: dict | None = None,
        skip: int = 0,
        limit: int = 100,
        unique: bool = False,
    ) -> Iterable[User] | list[None] | User: ...

    @abstractmethod
    async def update(
        self, id_: int, attributes: dict[str, Any] = None
    ) -> User | None: ...


@dataclass
class ORMUserRepository(BaseUserRepository, BaseORMRepository[User]):
    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, attributes: dict[str, Any] = None) -> User | None:
        return await super(BaseUserRepository, self).create(
            attributes=attributes
        )

    async def get_by_id(self, id_: int) -> User | None:
        return await super(BaseUserRepository, self).get_by(
            field="id", value=id_, unique=True
        )

    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] = None,
        order_: dict | None = None,
        skip: int = 0,
        limit: int = 100,
        unique: bool = False,
    ) -> Iterable[User] | list[None] | User:
        return await super(BaseUserRepository, self).get_by_filter(
            filter_params=filter_params,
            join_=join_,
            skip=skip,
            limit=limit,
            order_=order_,
            unique=unique,
        )

    async def update(self, id_, attributes=None):
        return await super(BaseUserRepository, self).update(id_, attributes)

    def _join_genres(self, query: Select):
        return query.options(joinedload(User.genres))
