from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from core.generics import ModelType
from core.repositories import BaseRepository


@dataclass
class BaseService(ABC):
    @abstractmethod
    async def create(self, attributes: dict[str, Any] = None): ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100): ...

    @abstractmethod
    async def delete(self, instance: Any) -> None: ...

    @abstractmethod
    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] | None = None,
        order_: dict | None = None,
        unique: bool = False,
    ): ...

    @abstractmethod
    async def get_by_id(self, id_: int): ...

    @abstractmethod
    async def update(self, id_: int, attributes: dict[str, Any] = None): ...


# ToDo добавить другие базовые crud методы
@dataclass
class BaseOrmService(BaseService):
    """Базовый класс сервисов для работы с данными"""

    repository: BaseRepository

    async def create(self, attributes: dict[str, Any] = None) -> ModelType:
        return await self.repository.create(attributes)

    async def get_all(self, skip: int = 0, limit: int = 100):
        return await self.repository.get_all()

    async def delete(self, instance: Any) -> None: ...

    async def get_by_id(
        self, id_: int, join_: set[str] | None = None
    ) -> ModelType:
        """
        Метод ищет инстанс в модели по айди

        :param id_: айди для поиска
        :param join_: соединения, которые нужно добавить
        :return: найденный инстанс
        """

        return await self.repository.get_by(
            field="id", value=id_, join_=join_, unique=True
        )

    async def get_by_filter(
        self,
        filter_params: dict,
        join_: set[str] | None = None,
        order_: dict | None = None,
        unique: bool = False,
    ) -> Iterable[ModelType] | ModelType:
        """
        Метод возвращает инстансы модели, отфильтрованные
        по значению одного или нескольких полей

        :param filter_params: поля и значения для фильтрации.
        Передаются в виде словаря поле:значение
        :param join_: список джоинов для связи.
        :param unique: нужно ли вернуть одно значение (первое) или их список
        :return: список инстансов или инстанс
        """
        return await self.repository.filter(
            filter_params=filter_params, join_=join_, unique=unique
        )

    async def update(
        self, id_: int, attributes: dict[str, Any] = None
    ) -> ModelType:
        """
        Метод для обновления инстанса модели.

        :param id_: id обновляемого инстанса
        :param attributes: аттрибуты обновляемого инстанса
        :return: возвращает обновлённый инстанс
        """
        return await self.repository.update(id_, attributes)
