from sys import stdout
from dataclasses import dataclass
from loguru import logger

from core.loggings.base import BaseLoggings

@dataclass
class MainLogger(BaseLoggings):

    def __set_handlers(self):
        return [
                {'sink': 
                    f'logs/{self.module_name}.log',
                    'rotation':'10 mb',
                    'level':'INFO',
                    'compression':'zip',
                    'retention':10,
                    'enqueue':True
                },
                {'sink':
                    stdout, 
                    "format": "{time} | {level} | {module} :: {function} : {line} - {message}",
                    'level':'DEBUG'
                },
                {'sink': 
                    f'logs/{self.module_name}_error.log',
                    'rotation':'5 mb',
                    'level':'ERROR',
                    'compression':'zip',
                    'encoding':'utf-8',
                    'serialize':True
                },
            ]

    def __set_configs(self):
        return {
            "handlers": self.__set_handlers(),
            "extra": {'ip': 'localhost'}
        }

    def __post_init__(self):
        self.log = logger
        self.handlers: list = self.__set_handlers()
        self.configs:  dict[str, Any] = self.__set_configs()

    def add_handler(self, handler: list):
        if self.handlers is not None:
            self.handlers.append(handler)

    def setup_config_loggers(self, config: dict):
        """Метод для настройки логера через конфиг
        """
        self.log.remove()
        self.log.configure(**config)
        return self
  
    def setup_lib_configs(self):
        """Метод для настройки логера через конфиг библиотеки
        """
        self.setup_config_loggers(self.configs)
        return self

    def get_full_format(self):
        return "{time} - [{level}] - {name} {module} - ({file} - {function}: {line}) {extra} - {message}"
