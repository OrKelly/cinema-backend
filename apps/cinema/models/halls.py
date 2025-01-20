from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base import Base
from core.database.mixins.id import IntegerIdMixin

if TYPE_CHECKING:
    from apps.films.models.films import Film


class Hall(Base, IntegerIdMixin):
    __tablename__ = "halls"

    title: Mapped[str] = mapped_column(String(45), unique=True)
    description: Mapped[str] = mapped_column(Text)

    films: Mapped[list["Film"]] = relationship("Film", back_populates="hall")
