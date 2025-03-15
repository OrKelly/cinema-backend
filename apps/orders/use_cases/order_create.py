from dataclasses import dataclass
from typing import Any

from apps.notifications.services.send_services.base import (
    BaseNotificationService,
)
from apps.orders.models.order import Order
from apps.orders.services.orders import (
    BaseOrderService,
    BaseOrderValidatorService,
)
from core.database import Propagation, Transactional
from core.enums.orders import OrderPaymentStatusEnum
from core.exceptions.payments import PaymentFailedException
from core.payment.base import BasePaymentService


@dataclass
class CreateOrderUseCase:
    service: BaseOrderService
    validator: BaseOrderValidatorService
    payment_service: BasePaymentService
    notification_service: BaseNotificationService

    @Transactional(propagation=Propagation.REQUIRED)
    async def execute(self, attributes: dict[str, Any]) -> Order:
        await self.validator.validate(attributes)
        order = await self.service.create(attributes)
        payment_status = self.payment_service.make_payment(attributes)
        if payment_status == OrderPaymentStatusEnum.PAID:
            # ToDo добавить формирование и отправку билета
            await self.service.update(
                id_=order.id,
                attributes={"payment_status": OrderPaymentStatusEnum.PAID},
            )
            await self.notificate(attributes)
            return order
        await self.service.update(
            id_=order.id,
            attributes={"payment_status": OrderPaymentStatusEnum.CANCELLED},
        )
        raise PaymentFailedException

    async def notificate(self, attributes: dict[str, Any]) -> None:
        # ToDo реализовать нотификацию после рефактора и добавления билетов
        ...
