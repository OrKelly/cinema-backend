from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base import Base
from core.database.mixins.id import IntegerIdMixin

# условие для обхода цикличного импорта
# (либо можно убрать relationship от зала к фильму)
if TYPE_CHECKING:
    from films import Film


class Hall(Base, IntegerIdMixin):
    __tablename__ = "halls"

    title: Mapped[str] = mapped_column(String(45))
    description: Mapped[str] = mapped_column(Text)

    film: Mapped["Film"] = relationship("Film", back_populates="halls")
