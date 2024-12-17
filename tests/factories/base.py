import inspect
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Generic, TypeVar

from core.database import get_session
from core.generics import ModelType

InstanceSchemaType = TypeVar(
    "InstanceSchemaType", bound="BaseFakeSchema", covariant=True
)

FactoryType = TypeVar("FactoryType", bound="BaseFactory")


@dataclass
class SubFactory:
    """Класс для создания и связывания объектов с помощью фабрик.
    Предназначен для использования с BaseFactory.

    :param: factory: Фабрика, которая будет использоваться для
    создания связанного объекта.
    :param: primary_key: Имя поля первичного ключа в связанной модели,
    значение которого будет использоваться.
    """

    factory: type[FactoryType]
    primary_key: str = "id"

    async def __call__(self, *args, **kwargs):
        return await self.create()

    async def create(self) -> str:
        instance = await self.factory().create()
        return getattr(instance, self.primary_key, None)


class BaseFakeSchemaMeta(type):
    """Метакласс для создания наследников базовой схемы.

    Нужен для получения списка собственных определенных аттрибутов и
    их дальнейшей обработки
    """

    # ToDo добавить рейз ошибок при отсутствии Meta model, и подумать
    #  над подобными моментами. В будущем подумать над
    #  упразднением этих классов и переноса всей логики в фабрики
    def __new__(cls, name, bases, attrs):
        _schema_attrs = {}
        meta_model = attrs["Meta"].model
        for attr_name, attr_value in attrs.items():
            if not attr_name.startswith("__") and hasattr(
                meta_model, attr_name
            ):
                _schema_attrs[attr_name] = attr_value

        attrs["_schema_attrs"] = _schema_attrs
        return super().__new__(cls, name, bases, attrs)


@dataclass
class BaseFakeSchema(metaclass=BaseFakeSchemaMeta):
    """Класс схем для генерации фейковых данных.

    Для использования - отнаследоваться и определить поля.
    Поля определяются по следующему принципу:

    поле - фабрика, или фиксированное значение.
    Для создания связанных моделей использовать
    подкласс SubFactory. Примеры:

    number - faker.pyint
    description - "Описание"
    hall_id - SubFactory(factory=HallFactory)
    """

    async def model_dump(self) -> dict:
        instance_data = {}
        for attr, factory in self._schema_attrs.items():
            if callable(factory):
                if inspect.isawaitable(factory) or isinstance(
                    factory, SubFactory
                ):
                    instance_data[attr] = await factory()
                else:
                    instance_data[attr] = factory()
            else:
                instance_data[attr] = factory

        return instance_data

    class Meta:
        model = type[ModelType]


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

    model_class: type[ModelType]
    schema: type[InstanceSchemaType]

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.schema = self.schema()

    async def create(self) -> type[ModelType]:
        async with get_session() as session:
            instance_data = await self.row()
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
        return await self.schema.model_dump()
