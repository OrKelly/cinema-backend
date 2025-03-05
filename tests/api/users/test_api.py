import pytest
from httpx import AsyncClient

from apps.users.services.users import BaseUserService
from core.containers import get_container
from tests.factories.genres import GenreFactory
from tests.factories.user import UserFactory

user_service = get_container().resolve(BaseUserService)


class TestUserApi:
    @staticmethod
    def get_list_url(*args, **kwargs):
        return "/".join(("api/v1/users", *map(str, args)))

    @pytest.mark.asyncio
    async def test_user_register(self, client: AsyncClient, faker):
        payload = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "password": faker.password(length=8, digits=True, upper_case=True),
            "email": faker.email(),
        }

        response = await client.post(
            self.get_list_url("register"), json=payload
        )
        assert response.status_code == 200
        user = await user_service.get_by_id(response.json()["data"]["id"])
        assert user.id == response.json()["data"]["id"]
        for attr, value in payload.items():
            if hasattr(user, attr) and attr != "password":
                assert getattr(user, attr) == value

    async def test_user_register_with_exist_email(
        self, client: AsyncClient, faker
    ):
        user = await UserFactory().create()
        payload = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "password": faker.password(length=8, digits=True, upper_case=True),
            "email": user.email,
        }
        response = await client.post(
            self.get_list_url("register"), json=payload
        )  # E501
        assert response.status_code == 409
        user = await user_service.get_by_email(payload["email"], unique=False)
        assert len(user) == 1

    async def test_user_register_with_bad_password(
        self, client: AsyncClient, faker
    ):
        payload = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "password": "simplepass",
            "email": faker.email(),
        }
        response = await client.post(
            self.get_list_url("register"), json=payload
        )  # E501
        assert response.status_code == 400
        user = await user_service.get_by_email(payload["email"])
        assert not user

    async def test_user_login(self, client: AsyncClient, faker):
        password = faker.password(length=8, digits=True, upper_case=True)
        user = await UserFactory(password=password).create()
        payload = {"email": user.email, "password": password}
        response = await client.post(self.get_list_url("login"), json=payload)
        assert response.status_code == 200

    async def test_user_login_with_wrong_password(
        self, client: AsyncClient, faker
    ):
        user = await UserFactory().create()
        payload = {"email": user.email, "password": faker.password()}
        response = await client.post(self.get_list_url("login"), json=payload)
        assert response.status_code == 401

    async def test_get_all_users(
        self, client: AsyncClient, faker, prepare_database
    ):
        amount_users = faker.pyint(max_value=20)
        await UserFactory().create_batch(amount_users)
        response = await client.get(self.get_list_url())
        response_json = response.json()["data"]
        assert response.status_code == 200
        assert len(response_json["users"]) == amount_users

    @pytest.mark.parametrize(
        "selected_genre_ids", [[1, 2, 3], [1, 3, 5, 8], [4, 8, 1]]
    )
    async def test_add_user_favourite_genres(
        self,
        selected_genre_ids,
        logged_client: AsyncClient,
    ):
        await GenreFactory().create_batch(instances_count=10)
        payload = {"genre_ids": selected_genre_ids}
        response = await logged_client.post(
            self.get_list_url("genres"), json=payload
        )  # E501
        response_json = response.json()["data"]
        assert response.status_code == 200
        assert response_json["genre_ids"] == selected_genre_ids

    async def test_add_already_exist_user_favourite_genres(
        self,
        prepare_database,
        logged_client: AsyncClient,
        faker,
    ):
        await GenreFactory().create_batch(instances_count=10)
        selected_genre_ids = list(
            {faker.random_int(min=1, max=10) for _ in range(7)}
        )
        payload = {"genre_ids": selected_genre_ids}
        await logged_client.post(
            self.get_list_url("genres"), json=payload
        )  # E501
        response = await logged_client.post(
            self.get_list_url("genres"), json=payload
        )  # E501
        response_json = response.json()["data"]
        assert response.status_code == 200
        assert response_json["genre_ids"] == selected_genre_ids

    async def test_add_user_favourite_genres_without_authentication(
        self,
        prepare_database,
        client: AsyncClient,
        faker,
    ):
        selected_genre_ids = list(
            {faker.random_int(min=1, max=10) for _ in range(7)}
        )
        payload = {"genre_ids": selected_genre_ids}
        response = await client.post(
            self.get_list_url("genres"), json=payload
        )  # E501
        assert response.status_code == 403
        assert response.json()["detail"] == "Доступ запрещен"
