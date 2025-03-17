from enum import Enum


class OrderPaymentStatusEnum(Enum):
    NOT_PAID = "Не оплачен"
    PENDING_PAYMENT = "Ожидание подтверждения оплаты"
    PAID = "Оплачен"
    CANCELLED = "Отменен"
