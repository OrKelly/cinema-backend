from .base import ServerException


class PaymentFailedException(ServerException):
    @property
    def message(self):
        return "Произошла ошибка при обработке платежа"
