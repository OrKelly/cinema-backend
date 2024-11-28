from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.mixins.id import IntegerIdMixin
from core.database.base import Base

# условие для обхода цикличного импорта
# (либо можно убрать взаимосвязь от жанра к фильму)
if TYPE_CHECKING:
    from films import Film


class FilmSession(Base, IntegerIdMixin):
    __tablename__ = 'filmsessions'

    film_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('films.id_film', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    place_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('places.id_film', onupdate='CASCADE', ondelete='SET NULL'),
    )
    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    price: Mapped[float] = mapped_column(Float)

    film: Mapped['Film'] = relationship('Film', back_populates='filmsessions')
