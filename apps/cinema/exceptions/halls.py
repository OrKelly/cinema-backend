from dataclasses import dataclass

from core.exceptions import NotFoundException


@dataclass
class HallNotFoundException(NotFoundException):
    hall_id: int = None

    @property
    def message(self):
        return f"Кинозал с айди {self.hall_id} не найден"
