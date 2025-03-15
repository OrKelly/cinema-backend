from typing import Any

from core.enums.orders import OrderPaymentStatusEnum
from core.payment.base import BasePaymentService


class MockPaymentService(BasePaymentService):
    """Мок класс платежки. Всегда возвращает "Оплачено".
    Заменить в системе после внесения конкретики"""

    def make_payment(self, attributes: dict[str, Any]):
        return OrderPaymentStatusEnum.PAID
