from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class BaseLoggings(ABC):
    """
    Базовый класс для логирования
    """

    module_name: str
    level: str | int = 'INFO'
    format: str = '{time} - {message}'

    @abstractmethod
    def setup_config_loggers(self, config: dict):
        """Метод для настройки логера через конфиг
        """
        ...

    @abstractmethod
    def setup_lib_configs(self):
        """Конфиг для логирования
        """
        ...

    @abstractmethod
    def get_full_format(self): ...
