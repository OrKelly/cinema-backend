from faker import Faker
from pydantic import BaseModel, Field

from apps.cinema.models.halls import Hall
from apps.cinema.models.rows import Row
from core.database import get_session
from tests.factories.base import BaseFactory

from .halls import HallCreate, HallFactory

fake = Faker(locale="ru_RU")


class RowCreate(BaseModel):
    hall_id: HallCreate
    number: int = Field(default_factory=fake.pyint)


class RowFactory(BaseFactory[Row, RowCreate]):
    model_class = Row
    schema = RowCreate

    async def create(self) -> Row:
        async with get_session() as session:
            instance_data = await self._get_instance_data()
            hall = Hall(**instance_data["hall_id"])
            session.add(hall)
            await session.commit()
            instance_data["hall_id"] = hall.id
            instance = self.model_class(**instance_data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def _get_instance_data(self) -> dict:
        instance_data = await self.__get_fake_instance_data()
        if self.kwargs:
            for attr, value in self.kwargs.items():
                if attr in instance_data:
                    instance_data[attr] = value
        return instance_data

    async def __get_fake_instance_data(self) -> dict:
        hall = await HallFactory()._get_instance_data()
        return self.schema(
            hall_id=HallCreate(
                title=hall["title"],
                description=hall["description"],
            )
        ).model_dump()
