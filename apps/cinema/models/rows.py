from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base import Base
from core.database.mixins.id import IntegerIdMixin

# условие для обхода цикличного импорта
# (либо можно убрать взаимосвязь)
if TYPE_CHECKING:
    from places import Place


class Row(Base, IntegerIdMixin):
    __tablename__ = "rows"

    hall_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("halls.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    number: Mapped[int] = mapped_column(Integer, nullable=False)

    places: Mapped[list["Place"]] = relationship("Place", back_populates="row")
