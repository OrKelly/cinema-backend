import pytest
from apps.users.services.users import BaseUserService
from httpx import AsyncClient
from tests.factories.user import UserFactory


class TestUserApi:
    @staticmethod
    def get_register_url(**kwargs):
        return "api/v1/users/register"

    @staticmethod
    def get_login_url(**kwargs):
        return "api/v1/users/login"

    @staticmethod
    def get_all_users_list_url(*args, **kwargs):
        return "api/v1/users/" + "/".join(map(str, args))

    @pytest.mark.asyncio
    async def test_user_register(self, client: AsyncClient, faker, container):
        payload = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "password": faker.password(length=8, digits=True, upper_case=True),
            "email": faker.email(),
        }

        response = await client.post(self.get_register_url(), json=payload)
        assert response.status_code == 200
        user_service = container.resolve(BaseUserService)
        user = await user_service.get_by_id(response.json()["data"]["id"])
        assert user.id == response.json()["data"]["id"]
        for attr, value in payload.items():
            if hasattr(user, attr) and attr != "password":
                assert getattr(user, attr) == value

    async def test_user_register_with_exist_email(
        self, client: AsyncClient, faker, container
    ):
        user = await UserFactory().create()
        payload = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "password": faker.password(length=8, digits=True, upper_case=True),
            "email": user.email,
        }
        response = await client.post(self.get_register_url(), json=payload)
        assert response.status_code == 409
        user_service = container.resolve(BaseUserService)
        user = await user_service.get_by_email(payload["email"], unique=False)
        assert len(user) == 1

    async def test_user_register_with_bad_password(
        self, client: AsyncClient, faker, container
    ):
        payload = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "password": "simplepass",
            "email": faker.email(),
        }
        response = await client.post(self.get_register_url(), json=payload)
        assert response.status_code == 400
        user_service = container.resolve(BaseUserService)
        user = await user_service.get_by_email(payload["email"])
        assert not user

    async def test_user_login(self, client: AsyncClient, faker):
        password = faker.password(length=8, digits=True, upper_case=True)
        user = await UserFactory(password=password).create()
        payload = {"email": user.email, "password": password}
        response = await client.post(self.get_login_url(), json=payload)
        assert response.status_code == 200

    async def test_user_login_with_wrong_password(self, client: AsyncClient, faker):
        user = await UserFactory().create()
        payload = {"email": user.email, "password": faker.password()}
        response = await client.post(self.get_login_url(), json=payload)
        assert response.status_code == 401

    async def test_get_all_users(self, client: AsyncClient, faker, prepare_datebase):
        amount_users = faker.pyint(max_value=20)
        await UserFactory().create_batch(amount_users)
        response = await client.get(self.get_all_users_list_url("users"))
        response_json = response.json()["data"]
        assert response.status_code == 200
        assert len(response_json["users"]) == amount_users
