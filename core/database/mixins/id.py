from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr


class IntegerIdMixin:
    """Миксин, добавляющий id pk"""

    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True, autoincrement=True)
