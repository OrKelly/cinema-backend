from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr


class TimeStampMixin:
    """Миксин, добавляющий автоматически заполняющиеся created_at и updated_at"""
    @declared_attr
    def created_at(self):
        return Column(DateTime, default=func.now(), nullable=False)

    @declared_attr
    def updated_at(self):
        return Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
