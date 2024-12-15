from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.database.base import Base
from core.database.mixins.id import IntegerIdMixin


class Hall(Base, IntegerIdMixin):
    __tablename__ = "halls"

    title: Mapped[str] = mapped_column(String(45), unique=True)
    description: Mapped[str] = mapped_column(Text)
