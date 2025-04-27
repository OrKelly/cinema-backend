from apps.cinema.exceptions.places import PlaceNotFoundException
from apps.films.exceptions.film_sessions import FilmSessionNotFoundException
from apps.orders.exceptions.orders import (
    PlaceAlreadyTakenException,
    UserAndEmailNotGivenException,
)
from apps.orders.models.order import Order
from apps.orders.services.orders import BaseOrderService
from tests.factories.film_sessions import FilmSessionFactory
from tests.factories.orders import OrderFactory
from tests.factories.place import PlaceFactory


class TestOrderAPI:
    @staticmethod
    def get_list_url(*args, **kwargs):
        return "api/v1/orders/" + "/".join(map(str, args))

    @staticmethod
    async def get_payload() -> dict:
        filmsession = await FilmSessionFactory().create()
        place = await PlaceFactory().create()
        return {"filmsession_id": filmsession.id, "place_ids": [place.id]}

    @staticmethod
    def compare_instances(order: Order, payload: dict):
        order_payload = {
            "filmsession_id": order.filmsession_id,
            "place_ids": [order.place_id],
        }
        return order_payload == payload

    async def test_create_with_exists_user(
        self, prepare_database, logged_client, container
    ):
        payload = await self.get_payload()

        service: BaseOrderService = container.resolve(BaseOrderService)
        orders = await service.get_all()
        assert not orders

        response = await logged_client.post(self.get_list_url(), json=payload)
        assert response.status_code == 200

        order = await service.get_by_id(
            id_=response.json()["data"]["order_ids"][0]
        )
        self.compare_instances(order, payload)

    async def test_create_with_email(
        self, prepare_database, client, container, faker
    ):
        payload = await self.get_payload()
        payload["email"] = faker.email()

        service: BaseOrderService = container.resolve(BaseOrderService)
        orders = await service.get_all()
        assert not orders

        response = await client.post(self.get_list_url(), json=payload)
        assert response.status_code == 200

        order = await service.get_by_id(
            id_=response.json()["data"]["order_ids"][0]
        )
        self.compare_instances(order, payload)

    async def test_create_without_email_and_user_id(
        self, prepare_database, client, container, faker
    ):
        payload = await self.get_payload()

        service: BaseOrderService = container.resolve(BaseOrderService)
        orders = await service.get_all()
        assert not orders

        response = await client.post(self.get_list_url(), json=payload)

        assert response.status_code == 400
        assert (
            response.json()["message"]
            == UserAndEmailNotGivenException().message
        )

        orders = await service.get_all()
        assert not orders

    async def test_create_with_not_exists_session(
        self, prepare_database, logged_client, container, faker
    ):
        payload = await self.get_payload()
        payload["filmsession_id"] = faker.pyint()

        service: BaseOrderService = container.resolve(BaseOrderService)
        orders = await service.get_all()
        assert not orders

        response = await logged_client.post(self.get_list_url(), json=payload)

        assert response.status_code == 404
        assert (
            response.json()["message"]
            == FilmSessionNotFoundException().message
        )

        orders = await service.get_all()
        assert not orders

    async def test_create_with_not_exists_place(
        self, prepare_database, logged_client, container, faker
    ):
        payload = await self.get_payload()
        payload["place_ids"].append(faker.pyint())

        service: BaseOrderService = container.resolve(BaseOrderService)
        orders = await service.get_all()
        assert not orders

        response = await logged_client.post(self.get_list_url(), json=payload)

        assert response.status_code == 404
        assert response.json()["message"] == PlaceNotFoundException().message

        orders = await service.get_all()
        assert not orders

    async def test_create_with_not_free_place(
        self, prepare_database, logged_client, container, faker
    ):
        order = await OrderFactory().create()
        payload = {
            "place_ids": [order.place_id],
            "filmsession_id": order.filmsession_id,
        }

        service: BaseOrderService = container.resolve(BaseOrderService)
        orders = await service.get_all()
        assert len(orders) == 1

        response = await logged_client.post(self.get_list_url(), json=payload)

        assert response.status_code == 400
        assert (
            response.json()["message"] == PlaceAlreadyTakenException().message
        )

        orders = await service.get_all()
        assert len(orders) == 1
