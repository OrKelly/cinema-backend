from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base import Base
from core.database.mixins.id import IntegerIdMixin

# условие для обхода цикличного импорта
# (либо можно убрать взаимосвязь от жанра к фильму)
if TYPE_CHECKING:
    from films import Film

    from apps.cinema.models import Hall


class FilmSession(Base, IntegerIdMixin):
    __tablename__ = "filmsessions"

    film_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("films.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    hall_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("halls.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    price: Mapped[float] = mapped_column(Numeric(10, 2))

    film: Mapped["Film"] = relationship("Film", back_populates="filmsessions")
    hall: Mapped["Hall"] = relationship("Hall", back_populates="filmsessions")
