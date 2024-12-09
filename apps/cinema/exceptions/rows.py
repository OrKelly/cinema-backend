from dataclasses import dataclass

from core.exceptions import NotFoundException


@dataclass
class RowNotFoundException(NotFoundException):
    row_id: int = None

    @property
    def message(self):
        return f"Ряд с айди {self.row_id} не найден"
