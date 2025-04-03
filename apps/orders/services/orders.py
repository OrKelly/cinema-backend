from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from apps.cinema.exceptions.places import PlaceNotFoundException
from apps.cinema.repositories.places import BasePlaceRepository
from apps.films.exceptions.film_sessions import FilmSessionNotFoundException
from apps.films.repositories.film_sessions import BaseFilmSessionRepository
from apps.orders.exceptions.orders import (
    OrderNotFoundException,
    PlaceAlreadyTakenException,
    UserAndEmailNotGivenException,
)
from apps.orders.models.order import Order
from apps.orders.repositories.orders import BaseOrderRepository
from apps.users.exceptions.users import UserNotFoundException
from apps.users.repositories.users import BaseUserRepository
from core.services.base import BaseOrmService


@dataclass
class BaseOrderService(ABC):
    repository: BaseOrderRepository

    @abstractmethod
    async def create(self, attributes: dict[str, Any]) -> Order: ...

    @abstractmethod
    async def get_by_id(
        self, id_: int, join_: set[str] | None = None
    ) -> Order | None: ...

    @abstractmethod
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ) -> Iterable[Order] | Order | None: ...

    @abstractmethod
    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] = None,
        order_: dict | None = None,
        unique: bool | None = False,
    ): ...

    @abstractmethod
    async def update(
        self, id_: int, attributes: dict[str, Any]
    ) -> Order | None: ...


@dataclass
class ORMOrderService(BaseOrderService, BaseOrmService):
    async def create(self, attributes: dict[str, Any]):
        return await super(BaseOrderService, self).create(attributes)

    async def get_by_id(
        self, id_, join_: set[str] | None = None
    ) -> Order | None:
        order = await super(BaseOrderService, self).get_by_id(
            id_=id_, join_=join_
        )
        if not order:
            raise OrderNotFoundException()
        return order

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        join_: set[str, Any] = None,
        order_: dict | None = None,
    ) -> Iterable[Order] | Order | None:
        return await super(BaseOrderService, self).get_all(
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
        return await super(BaseOrderService, self).get_by_filter(
            filter_params=filter_params, join_=join_, order_=order_
        )

    async def update(
        self, id_: int, attributes: dict[str, Any]
    ) -> Order | None:
        return await super(BaseOrderService, self).update(
            id_=id_, attributes=attributes
        )


@dataclass
class BaseOrderValidatorService(ABC):
    @abstractmethod
    async def validate(self, attributes: dict[str, Any]) -> None: ...


@dataclass
class ExistsUserValidatorService(BaseOrderValidatorService):
    user_repository: BaseUserRepository

    async def validate(self, attributes: dict[str, Any]) -> None:
        if user_id := attributes.get("user_id"):
            user = await self.user_repository.get_by_id(user_id)
            if not user:
                raise UserNotFoundException()


@dataclass
class ExistsFilmSessionValidatorService(BaseOrderValidatorService):
    session_repository: BaseFilmSessionRepository

    async def validate(self, attributes: dict[str, Any]) -> None:
        filmsession_id = attributes.get("filmsession_id")
        session = await self.session_repository.get_by_id(id_=filmsession_id)
        if not session:
            raise FilmSessionNotFoundException


@dataclass
class ExistsUserOrEmailValidatorService(BaseOrderValidatorService):
    async def validate(self, attributes: dict[str, Any]) -> None:
        if not attributes.get("user_id") and not attributes.get("email"):
            raise UserAndEmailNotGivenException


@dataclass
class ExistsPlaceValidatorService(BaseOrderValidatorService):
    place_repository: BasePlaceRepository

    async def validate(self, attributes: dict[str, Any]) -> None:
        place_id = attributes.get("place_id")
        place = await self.place_repository.get_by_id(place_id)
        if not place:
            raise PlaceNotFoundException


@dataclass
class PlaceIsFreeValidatorService(BaseOrderValidatorService):
    order_repository: BaseOrderRepository

    async def validate(self, attributes: dict[str, Any]) -> None:
        place_id = attributes.get("place_id")
        filmsession_id = attributes.get("filmsession_id")
        orders = await self.order_repository.get_by_filter(
            filter_params={
                "place_id": place_id,
                "filmsession_id": filmsession_id,
            }
        )
        if orders:
            raise PlaceAlreadyTakenException


@dataclass
class ComposedOrderValidatorService(BaseOrderValidatorService):
    validators: Iterable[BaseOrderValidatorService]

    async def validate(self, attributes: dict[str, Any]) -> None:
        for validator in self.validators:
            await validator.validate(attributes)
