from core.exceptions.base import (
    InstanceAlreadyExistException,
    NotFoundException,
)


class TicketNotFoundException(NotFoundException):
    @property
    def message(self):
        return "Билет не найден!"


class TicketForOrderAlreadyExistException(InstanceAlreadyExistException):
    @property
    def message(self):
        return "На этот заказ уже существует билет!"
