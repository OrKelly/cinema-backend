from dataclasses import dataclass

from core.exceptions import NotFoundException
from core.exceptions.base import InstanceAlreadyExistException


@dataclass
class RowNotFoundException(NotFoundException):
    @property
    def message(self):
        return "Ряд с указанными параметрами не найден"


@dataclass
class RowAlreadyExistsException(InstanceAlreadyExistException):
    @property
    def message(self):
        return "Ряд с таким номером уже существует"
