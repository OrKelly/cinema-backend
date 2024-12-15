from collections.abc import Iterable
from dataclasses import dataclass
from typing import Generic, TypeVar

from core.database import get_session
from core.generics import ModelType

InstanceSchemaType = TypeVar("InstanceSchemaType")

FactoryType = TypeVar("FactoryType", bound="BaseFactory")


@dataclass
class SubFactory:
    """Класс для создания и связывания объектов с помощью фабрик.
    Предназначен для использования с BaseFactory.

    :param: factory: Фабрика, которая будет использоваться для
    создания связанного объекта.
    :param: foreign_key: Имя поля внешнего ключа в основной модели,
    куда будет записан id.
    :param: primary_key: Имя поля первичного ключа в связанной модели,
    значение которого будет использоваться.
    """

    factory: type(FactoryType)
    foreign_key: str
    primary_key: str = "id"

    async def create(self) -> str:
        instance = await self.factory().create()
        return getattr(instance, self.primary_key, None)


class BaseFactory(Generic[ModelType, InstanceSchemaType]):
    """
    Базовый класс для генерации инстансов моделей для тестов
    Для использования отнаследуйтесь от него и определите model_class и schema
    По необходимости - переопределить/расширить метод row

    :param model_class: Модель
    :param schema: Схема, которая создает фейковые данные
    :param sub_factories: Подфабрики, используемые
    для создания связанных моделей.
    """

    model_class: ModelType
    schema: InstanceSchemaType
    sub_factories: Iterable[SubFactory] = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    async def create(self) -> type[ModelType]:
        async with get_session() as session:
            instance_data = await self.row()
            for factory in self.sub_factories:
                instance_data[factory.foreign_key] = await factory.create()
            instance = self.model_class(**instance_data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def create_batch(self, instances_count: int) -> Iterable[ModelType]:
        instances = []
        async with get_session() as session:
            for _i in range(instances_count):
                instance_data = await self.row()
                for factory in self.sub_factories:
                    instance_data[factory.foreign_key] = await factory.create()
                instance = self.model_class(**instance_data)
                session.add(instance)
                instances.append(instance)
            await session.commit()
        return instances

    async def row(self) -> dict:
        instance_data = await self._get_instance_data()
        if self.kwargs:
            for attr, value in self.kwargs.items():
                if attr in instance_data:
                    instance_data[attr] = value
        return instance_data

    async def _get_instance_data(self) -> dict:
        return self.schema().model_dump()
