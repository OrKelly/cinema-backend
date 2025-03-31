from dataclasses import dataclass
from typing import Any

from apps.mail_service.base import BaseMailClient
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
    notification_service: BaseMailClient

    @Transactional(propagation=Propagation.REQUIRED)
    async def execute(self, attributes: dict[str, Any]) -> list[int]:
        order_ids = []
        while attributes.get("place_ids"):
            order_attributes = {
                attr: value
                for attr, value in attributes.items()
                if attr != "place_ids"
            }
            order_attributes["place_id"] = attributes.get("place_ids").pop()

            await self.validator.validate(attributes=order_attributes)
            order = await self.service.create(attributes=order_attributes)
            payment_status = self.payment_service.make_payment(
                attributes=order_attributes
            )
            if payment_status == OrderPaymentStatusEnum.PAID:
                # ToDo добавить формирование и отправку билета
                await self.service.update(
                    id_=order.id,
                    attributes={"payment_status": OrderPaymentStatusEnum.PAID},
                )
                await self.notificate(attributes=order_attributes)
                order_ids.append(order.id)
                continue
            await self.service.update(
                id_=order.id,
                attributes={
                    "payment_status": OrderPaymentStatusEnum.CANCELLED
                },
            )
            raise PaymentFailedException
        return order_ids

    async def notificate(self, attributes: dict[str, Any]) -> None:
        # ToDo реализовать нотификацию после рефактора и добавления билетов
        ...
