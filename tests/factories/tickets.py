from dataclasses import dataclass

from faker import Faker

from apps.orders.models import Ticket
from tests.factories.base import BaseFactory, BaseFakeSchema, SubFactory
from tests.factories.orders import OrderFactory

fake = Faker(locale="ru_RU")


@dataclass
class TicketCreate(BaseFakeSchema):
    order_id = SubFactory(factory=OrderFactory)
    file = fake.word

    class Meta:
        model = Ticket


class TicketFactory(BaseFactory[Ticket, TicketCreate]):
    model_class = Ticket
    schema = TicketCreate
