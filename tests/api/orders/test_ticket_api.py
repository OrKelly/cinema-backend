from sqlalchemy.exc import IntegrityError

from apps.orders.exceptions.tickets import TicketNotFoundException
from apps.orders.services.tickets import BaseTicketService
from tests.factories.orders import OrderFactory
from tests.factories.tickets import TicketFactory


class TestTicketAPI:
    async def test_create_ticket(self, prepare_database, container):
        ticket_service: BaseTicketService = container.resolve(
            BaseTicketService
        )
        all_ticket_before_create = await ticket_service.get_all()
        assert len(list(all_ticket_before_create)) == 0
        ticket = await TicketFactory().create()
        assert isinstance(ticket.order_id, int)
        assert isinstance(ticket.file, str)
        all_ticket_after_create = await ticket_service.get_all()
        assert len(list(all_ticket_after_create)) == 1

    async def test_create_second_ticket_order(
        self, prepare_database, container
    ):
        ticket_service: BaseTicketService = container.resolve(
            BaseTicketService
        )
        order = await OrderFactory().create()
        order_id = order.id
        await TicketFactory(order_id=order_id).create()
        try:
            await TicketFactory(order_id=order_id).create()
        except IntegrityError as e:
            answer = e.args[0].split("\n")[0].split(": ")[1]
            assert (
                answer
                == 'повторяющееся значение ключа нарушает ограничение уникальности "tickets_order_id_key"'  # noqa: E501
            )

        all_tickets = await ticket_service.get_all()

        assert len(list(all_tickets)) == 1

    async def test_get_by_id_not_exists_ticket(
        self, prepare_database, container, faker
    ):
        ticket_service: BaseTicketService = container.resolve(
            BaseTicketService
        )
        try:
            await ticket_service.get_by_id(id_=faker.pyint())
        except TicketNotFoundException as e:
            assert e.message == "Билет не найден!"  # noqa: PT017
