from faker import Faker

from apps.users.models.users import User
from core.security.password import PasswordHandler
from tests.factories.base import BaseFactory, BaseFakeSchema

fake = Faker(locale="ru_RU")


def generate_password():
    return fake.password(length=8, digits=True, upper_case=True)


class UserCreate(BaseFakeSchema):
    first_name: str = fake.first_name
    last_name: str = fake.last_name
    patronymic: str = fake.middle_name
    email: str = fake.email
    password: str = generate_password

    class Meta:
        model = User


class UserFactory(BaseFactory[User, UserCreate]):
    model_class = User
    schema = UserCreate

    async def row(self) -> dict:
        instance_data = await super().row()
        instance_data["password"] = PasswordHandler.hash(
            instance_data["password"]
        )
        return instance_data
