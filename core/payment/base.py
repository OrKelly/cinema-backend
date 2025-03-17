from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class BasePaymentService(ABC):
    # ToDo пока не до конца ясно, как работать с платежкой.
    # После конкретики - чуть поменять
    @abstractmethod
    def make_payment(self, attributes: dict[str, Any]): ...
