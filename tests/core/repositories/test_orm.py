import random
from typing import cast

import pytest
from faker import Faker

from apps.users.models.users import User
from core.generics import ModelType
from core.repositories.base import BaseORMRepository
from tests.factories.user import UserFactory

faker = Faker(locale="ru_RU")


class TestBaseORMRepository:
    async def test_create(self):
        attrs = await UserFactory().row()
        repository = BaseORMRepository(model_class=cast(ModelType, User))
        user = await repository.create(attributes=attrs)
        assert user
        assert await repository.get_by(field="id", value=user.id, unique=True)
        for attr, value in attrs.items():
            if hasattr(user, attr):
                assert getattr(user, attr) == value

    async def test_get_all(self, prepare_database):
        instances_count = random.randint(5, 10)
        await UserFactory().create_batch(instances_count=instances_count)
        repository = BaseORMRepository(model_class=cast(ModelType, User))
        users = await repository.get_all()
        assert users
        assert len(users) == instances_count

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("first_name", faker.first_name()),
            ("last_name", faker.last_name()),
            ("patronymic", faker.middle_name()),
        ],
    )
    async def test_get_by_many(self, field, value, prepare_database):
        instances_count = random.randint(5, 10)
        await UserFactory(**{field: value}).create_batch(
            instances_count=instances_count
        )
        repository = BaseORMRepository(model_class=cast(ModelType, User))
        users = await repository.get_by(field=field, value=value)
        assert users
        assert len(users) == instances_count

    @pytest.mark.parametrize(
        "filter_param",
        [
            {"first_name": faker.first_name()},
            {"last_name": faker.last_name()},
            {"first_name": faker.first_name(), "last_name": faker.last_name()},
            {
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "patronymic": faker.middle_name(),
            },
        ],
    )
    async def test_filter(self, filter_param, prepare_database):
        instances_count = random.randint(5, 10)
        await UserFactory(**filter_param).create_batch(instances_count)
        await UserFactory().create_batch(random.randint(1, 5))
        repository = BaseORMRepository(model_class=cast(ModelType, User))

        users = await repository.filter(filter_params=filter_param)
        assert len(users) == instances_count

    @pytest.mark.parametrize(
        "new_attrs",
        [
            {"first_name": faker.first_name(), "last_name": faker.last_name()},
        ],
    )
    async def test_update(self, new_attrs):
        attrs = await UserFactory().row()
        repository = BaseORMRepository(model_class=cast(ModelType, User))
        user = await repository.create(attributes=attrs)

        current_user_id = user.id
        update_user = await repository.update(current_user_id, new_attrs)

        assert attrs["first_name"] != update_user.first_name
        assert attrs["last_name"] != update_user.last_name
        assert new_attrs["first_name"] == update_user.first_name
        assert new_attrs["last_name"] == update_user.last_name
