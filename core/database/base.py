from enum import Enum

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def to_dict(self):
        return {
            column.name: self.enum_to_string(getattr(self, column.name))
            for column in self.__table__.columns
        }

    @staticmethod
    def enum_to_string(value):
        if isinstance(value, Enum):
            return value.value
        return value
