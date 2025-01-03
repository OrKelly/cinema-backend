from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseLogger(ABC):
    """
    Базовый класс для логирования
    """

    module_name: str

    @abstractmethod
    def setup_config_loggers(self, config: dict):
        """Метод для настройки логера через конфиг"""
        ...

    @abstractmethod
    def trace(self, message: str): ...

    @abstractmethod
    def debug(self, message: str):
        """Конфиг debug метод"""
        ...

    @abstractmethod
    def info(self, message: str): ...

    @abstractmethod
    def success(self, message: str): ...

    @abstractmethod
    def warning(self, message: str): ...

    @abstractmethod
    def error(self, message: str): ...

    @abstractmethod
    def critical(self, message: str): ...
