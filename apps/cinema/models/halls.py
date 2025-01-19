from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base import Base
from core.database.mixins.id import IntegerIdMixin

# условие для обхода цикличного импорта
# (либо можно убрать взаимосвязь)
if TYPE_CHECKING:
    from rows import Row


class Hall(Base, IntegerIdMixin):
    __tablename__ = "halls"

    title: Mapped[str] = mapped_column(String(45), unique=True)
    description: Mapped[str] = mapped_column(Text)

    rows: Mapped[list["Row"]] = relationship("Row", back_populates="hall")
