from dataclasses import dataclass

from core.exceptions.base import ServerException


@dataclass
class StartDateIncorrectException(ServerException):
    @property
    def message(self):
        return "Дата начала проката не может быть раньше сегодняшнего дня"


@dataclass
class EndDateIncorrectException(ServerException):
    @property
    def message(self):
        return (
            "Дата окончания проката не может быть раньше даты начала проката"
        )
