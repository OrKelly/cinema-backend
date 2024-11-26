from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base import Base

# условие для обхода цикличного импорта
# (либо можно убрать взаимосвязь от жанра к фильму)
if TYPE_CHECKING:
    from films import Film
    from apps.cinema.models.places import Place


class FilmSession(Base):
    __tablename__ = 'filmsessions'
    id_filmsession: Mapped[int] = mapped_column(Integer, primary_key=True)
    film_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('films.id_film', ondelete='CASCADE'),
        nullable=False
    )
    place_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('places.id_film', ondelete='SET NULL'),
    )
    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    price: Mapped[float] = mapped_column(Float)  # здесь больше подходит флоат (в схемах инт)

    film: Mapped['Film'] = relationship('Film', back_populates='filmsessions')
    places: Mapped[List['Place']] = relationship('Place')
