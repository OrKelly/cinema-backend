from dataclasses import dataclass
from datetime import datetime

from faker import Faker

from apps.orders.models.order import Order
from tests.factories.base import BaseFactory, BaseFakeSchema, SubFactory

from .film_sessions import FilmSessionFactory
from .place import PlaceFactory

fake = Faker(locale="ru_RU")


@dataclass
class OrderCreate(BaseFakeSchema):
    session_id = SubFactory(factory=FilmSessionFactory)
    place_id = SubFactory(factory=PlaceFactory)
    create_time: datetime = fake.date_time

    class Meta:
        model = Order


class OrderFactory(BaseFactory[Order, OrderCreate]):
    model_class = Order
    schema = OrderCreate
