from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseUseCase(ABC):
    """Базовый класс юз кейса"""

    @abstractmethod
    def execute(self): ...
