from dataclasses import dataclass

from core.exceptions import NotFoundException
from core.exceptions.base import InstanceAlreadyExistException


@dataclass
class RowNotFoundException(NotFoundException):
    row_id: int = None

    @property
    def message(self):
        return f"Ряд с айди {self.row_id} не найден"


@dataclass
class RowAlreadyExists(InstanceAlreadyExistException):
    row_number: int = None

    @property
    def message(self):
        return f"Ряд с номером {self.row_number} уже существует"
